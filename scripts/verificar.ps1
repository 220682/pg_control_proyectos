<#
.SYNOPSIS
  Consulta al verificador (Jev) antes de una accion irreversible. Solo veta; nunca autoriza.

.DESCRIPTION
  El script reune los HECHOS por su cuenta (git y el archivo del plan); el agente solo aporta la
  descripcion de la accion. Aplica los umbrales del estandar:
    todas las preguntas >= 0,9  -> CONTINUAR  (exit 0)
    alguna <= 0,1               -> BLOQUEAR   (exit 1)
    alguna entre 0,1 y 0,9      -> ESCALAR    (exit 2)
    sin respuesta / sin clave   -> SIN RESPUESTA (exit 3; quien llama decide segun la politica de fallo)

  Ver docs/00-estandar-agentes/07-verificador-de-acciones.md y docs/01-contexto-repositorio/07-jev-verificador.md.

.EXAMPLE
  .\scripts\verificar.ps1 -Clase merge -Accion "git merge local-worker-2 en main y push sin force" -Plan docs\02-trabajo-activo\01-planes\2026-09-30-tema.md
#>
param(
  [Parameter(Mandatory = $true)][ValidateSet('merge', 'push', 'borrar', 'migrar', 'rama', 'cierre')][string]$Clase,
  [Parameter(Mandatory = $true)][string]$Accion,
  [string]$Plan = '',
  [string]$Archivo = '',
  [string]$OtroRepo = '',
  [string]$Registro = ''
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$modelo = 'typesafe/jev-1.13'
$umbralSi = 0.9
$umbralNo = 0.1

function Redactar([string]$t) {
  $t = $t -replace 'sk-or-[A-Za-z0-9\-_]+', '[REDACTED]'
  $t = $t -replace '(?i)(api[_-]?key|token|password|passwd|secret|authorization)\s*[=:]\s*\S+', '$1=[REDACTED]'
  $t = $t -replace '(?i)\S*(entorno_variable|\.env)\S*', '[RUTA-SENSIBLE]'
  return $t
}

function Estado-Repo([string]$repo) {
  $r = [ordered]@{}
  try {
    $r.repositorio = Split-Path (git -C $repo rev-parse --show-toplevel) -Leaf
    $rama = (git -C $repo rev-parse --abbrev-ref HEAD).Trim()
    $r.rama_actual = $rama
    $cambios = @(git -C $repo status --porcelain).Count
    $r.arbol_de_trabajo = if ($cambios -eq 0) { 'limpio' } else { "$cambios cambios sin commitear" }
    $conteo = git -C $repo rev-list --left-right --count "origin/$rama...$rama" 2>$null
    if ($LASTEXITCODE -eq 0 -and $conteo) {
      $p = ($conteo -split '\s+')
      $r.commits_sin_bajar = [int]$p[0]
      $r.commits_sin_subir = [int]$p[1]
    } else {
      $r.commits_sin_subir = 'sin rama remota'
    }
  } catch {
    $r.error_git = 'no se pudo leer el estado de git'
  }
  return $r
}

function Gate([string]$texto, [string]$n) {
  $m = [regex]::Match($texto, "(?im)^\s*[-*]?\s*\**Gate $n\**\s*:\s*(.*)$")
  if (-not $m.Success) { return 'no consta' }
  $l = $m.Groups[1].Value
  if ($l -match '(?i)pendiente') { return 'pendiente' }
  if ($l -match '(?i)aprobad') { return 'aprobado' }
  return 'no consta'
}

# ---------- hechos ----------
$hechos = [ordered]@{}
$hechos.clase_de_accion = $Clase
$hechos.estado_git = Estado-Repo '.'
if ($OtroRepo) { $hechos.estado_git_otro_repositorio = Estado-Repo $OtroRepo }

$planTxt = ''
if ($Plan -and (Test-Path $Plan)) {
  $planTxt = Get-Content -Raw -Encoding UTF8 $Plan
  $hechos.gate_1 = Gate $planTxt '1'
  $hechos.gate_2 = Gate $planTxt '2'
  # Arreglo (Tanda V): por convención el informe del Auditor usa el nombre base del plan
  # sin el sufijo `-plan`; se aceptan ambos nombres (con y sin `-plan`) para no bloquear el Gate 2.
  $leaf = Split-Path $Plan -Leaf
  $auditoriaDir = Join-Path (Split-Path (Split-Path $Plan -Parent) -Parent) '04-auditoria'
  $candidatos = @((Join-Path $auditoriaDir ($leaf -replace '-plan\.md$', '.md')), (Join-Path $auditoriaDir $leaf))
  $informe = $candidatos | Where-Object { Test-Path $_ } | Select-Object -First 1
  if ($informe) {
    $it = Get-Content -Raw -Encoding UTF8 $informe
    $hechos.informe_de_auditoria = if ($it -match 'APLICAR AHORA' -and $it -match 'PROPONER A (RESPONSABLE|VICTOR)') { 'emitido con clasificación' } else { 'emitido sin clasificación' }
  } else {
    $hechos.informe_de_auditoria = 'no existe'
  }
  # Arreglo (Tanda V): el libro de hallazgos escribe el estado entre acentos graves
  # (`Registrada`); el patrón ahora acepta el estado con o sin acentos graves para contar las filas.
  $hechos.filas_de_hallazgos_sin_trasladar = ([regex]::Matches($planTxt, '\|\s*`?Registrada`?\s*\|')).Count
} else {
  $hechos.plan = 'no se indicó o no existe'
}

$accionSana = Redactar $Accion
$palabras = @(([regex]::Matches($accionSana, '[\w./\\-]{4,}') | ForEach-Object { $_.Value }) | Where-Object { $_ -notmatch '^(git|push|merge|force|branch|worktree|remove|main)$' })
$mencionada = $false
foreach ($w in $palabras) { if ($planTxt -and $planTxt.Contains($w)) { $mencionada = $true; break } }

$q = [ordered]@{}
switch ($Clase) {
  { $_ -in 'merge', 'push' } {
    $q.sin_dano = @{ type = 'noul'; instructions = 'La acción de state.accion es un merge o push normal: no usa force (--force, --force-with-lease o refspec con +), no borra ramas ni historial y no sobrescribe commits ajenos.'; criteria = @{ 'true' = 'Es un merge o push normal, sin force y sin borrar nada.'; 'false' = 'Usa force, borra ramas o historial, o puede perder commits.' } }
    $q.autorizada = @{ type = 'noul'; instructions = 'Los hechos de state.hechos_verificados muestran que se cumplen todas las condiciones para esta acción: gate_2 aprobado, informe_de_auditoria emitido con clasificación, árbol de trabajo limpio y cero commits sin subir.'; criteria = @{ 'true' = 'Todas las condiciones constan como cumplidas.'; 'false' = 'Falta alguna condición o consta como pendiente o inexistente.' } }
  }
  'borrar' {
    $hechos.el_plan_menciona_el_objetivo = $mencionada
    $q.alcance = @{ type = 'noul'; instructions = 'La acción de state.accion borra o reescribe solo lo que el plan menciona expresamente (state.hechos_verificados.el_plan_menciona_el_objetivo es verdadero), no usa force sobre ramas compartidas y no toca archivos de otro Worker.'; criteria = @{ 'true' = 'El plan menciona el objetivo y la acción se limita a él.'; 'false' = 'El plan no lo menciona, la acción es más amplia que lo autorizado o usa force.' } }
  }
  'migrar' {
    $destructivas = @()
    if ($Archivo -and (Test-Path $Archivo)) {
      $sql = Get-Content -Raw -Encoding UTF8 $Archivo
      $destructivas = @([regex]::Matches($sql, '(?i)\b(drop\s+(table|column|function|index|schema)|truncate|delete\s+from|rename\s+(to|column)|alter\s+table\s+\S+\s+drop)\b') | ForEach-Object { $_.Value.ToLower() } | Select-Object -Unique)
      $hechos.archivo_de_migracion = Split-Path $Archivo -Leaf
    } else {
      $hechos.archivo_de_migracion = 'no se indicó o no existe'
    }
    $hechos.sentencias_destructivas_encontradas = $destructivas
    $q.aditiva = @{ type = 'noul'; instructions = 'La migración de state.hechos_verificados.archivo_de_migracion es aditiva e idempotente: no borra ni renombra tablas o columnas y no elimina datos (sentencias_destructivas_encontradas está vacía).'; criteria = @{ 'true' = 'No hay sentencias destructivas y el archivo existe.'; 'false' = 'Hay sentencias destructivas o no se pudo revisar el archivo.' } }
    $q.autorizada = @{ type = 'noul'; instructions = 'gate_1 consta aprobado en state.hechos_verificados, lo que autoriza que los Workers apliquen las migraciones del plan.'; criteria = @{ 'true' = 'gate_1 aprobado.'; 'false' = 'gate_1 pendiente o no consta.' } }
  }
  'rama' {
    $hechos.el_plan_nombra_la_rama_o_carpeta = $mencionada
    $q.autorizada = @{ type = 'noul'; instructions = 'Crear, renombrar o borrar esta rama o worktree está autorizado: gate_1 consta aprobado y el plan nombra la rama o carpeta (el_plan_nombra_la_rama_o_carpeta es verdadero).'; criteria = @{ 'true' = 'gate_1 aprobado y el plan nombra el recurso.'; 'false' = 'Falta la aprobación o el plan no lo nombra.' } }
  }
  'cierre' {
    $q.listo = @{ type = 'noul'; instructions = 'Constan todas las condiciones para escribir el mensaje de cierre: gate_2 aprobado, informe_de_auditoria emitido con clasificación, filas_de_hallazgos_sin_trasladar igual a 0, árbol limpio y cero commits sin subir en cada repositorio revisado.'; criteria = @{ 'true' = 'Todas constan como cumplidas.'; 'false' = 'Falta alguna o consta como no cumplida.' } }
  }
}

# ---------- llamada ----------
function Salir([int]$codigo, [string]$resumen) {
  Write-Output $resumen
  if ($Registro) {
    Add-Content -Encoding UTF8 -Path $Registro -Value ((Get-Date -Format 'yyyy-MM-dd HH:mm') + ' | ' + $resumen)
  }
  exit $codigo
}

$clave = [Environment]::GetEnvironmentVariable('OPENROUTER_API_KEY', 'Process')
if (-not $clave) { $clave = [Environment]::GetEnvironmentVariable('OPENROUTER_API_KEY', 'User') }
if (-not $clave) { Salir 3 "SIN RESPUESTA [$Clase]: no hay clave OPENROUTER_API_KEY en el entorno" }

$cuerpo = @{ model = $modelo; state = @{ accion = $accionSana; hechos_verificados = $hechos }; questions = $q } | ConvertTo-Json -Depth 12
try {
  $r = Invoke-RestMethod -Method Post -Uri 'https://openrouter.ai/api/alpha/decisions' -Headers @{ Authorization = "Bearer $clave" } -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($cuerpo)) -TimeoutSec 30
} catch {
  Salir 3 ("SIN RESPUESTA [$Clase]: " + (Redactar $_.Exception.Message))
}

$valores = [ordered]@{}
foreach ($k in $q.Keys) { $valores[$k] = [double]$r.answers.$k.noul }
$texto = ($valores.GetEnumerator() | ForEach-Object { '{0}={1:N2}' -f $_.Key, $_.Value }) -join ' '
$minimo = ($valores.Values | Measure-Object -Minimum).Minimum

$ctx = "$modelo | $Clase | $accionSana"
if ($minimo -le $umbralNo) { Salir 1 "BLOQUEAR [$Clase] $texto | $ctx" }
elseif ($minimo -ge $umbralSi) { Salir 0 "CONTINUAR [$Clase] $texto | $ctx" }
else { Salir 2 "ESCALAR [$Clase] $texto | $ctx" }
