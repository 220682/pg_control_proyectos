<#
.SYNOPSIS
  Adaptador del hook PreToolUse: decide si una orden de Bash o PowerShell debe pasar por el verificador.

.DESCRIPTION
  Lee de la entrada estandar el JSON del hook. Solo interviene en las acciones reservadas a una puerta:
    - En el repositorio de la app (py_control_proyectos_web): merge a main, push a main, push con force,
      borrar ramas o worktrees, aplicar migraciones (migrar_*.py apply).
    - En cualquier repositorio: push con force, borrar ramas o worktrees, borrado recursivo.
  Todo lo demas pasa sin tocar nada (exit 0 sin salida).
  Responde con deny / ask / allow segun el codigo de scripts/verificar.ps1.

  NO esta registrado en ninguna configuracion. Ver docs/01-contexto-repositorio/07-jev-verificador.md.
#>
$ErrorActionPreference = 'Stop'
$entrada = [Console]::In.ReadToEnd() | ConvertFrom-Json
$cmd = [string]$entrada.tool_input.command
$cwd = if ($entrada.cwd) { [string]$entrada.cwd } else { (Get-Location).Path }
if (-not $cmd) { exit 0 }

function Responder([string]$decision, [string]$motivo) {
  @{ hookSpecificOutput = @{ hookEventName = 'PreToolUse'; permissionDecision = $decision; permissionDecisionReason = $motivo } } | ConvertTo-Json -Depth 5
  exit 0
}

$repo = ''
try { $repo = Split-Path (git -C $cwd rev-parse --show-toplevel 2>$null) -Leaf } catch { }
$esApp = $repo -eq 'py_control_proyectos_web'
$rama = ''
try { $rama = (git -C $cwd rev-parse --abbrev-ref HEAD 2>$null).Trim() } catch { }

$clase = ''
$destructiva = $false
if ($cmd -match 'git\s+push\b.*(--force\b|--force-with-lease|\s-f\b|\s\+\S)') { $clase = 'push'; $destructiva = $true }
elseif ($cmd -match 'git\s+(branch\s+(-d|-D|--delete)\b|worktree\s+remove\b|push\b.*--delete\b)') { $clase = 'borrar'; $destructiva = $true }
elseif ($cmd -match '(rm\s+-[a-z]*r[a-z]*f|rm\s+-[a-z]*f[a-z]*r|Remove-Item\b.*-Recurse)') { $clase = 'borrar'; $destructiva = $true }
elseif ($cmd -match 'migrar_[\w\-]+\.py\s+apply') { $clase = 'migrar'; $destructiva = $true }
elseif ($esApp -and $rama -eq 'main' -and $cmd -match 'git\s+merge\b') { $clase = 'merge' }
elseif ($esApp -and $cmd -match 'git\s+push\b.*\b(main|origin\s+main)\b') { $clase = 'push' }
elseif ($esApp -and $cmd -match 'git\s+(branch|worktree\s+add)\b') { $clase = 'rama' }

if (-not $clase) { exit 0 }

$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$plan = $env:PLAN_ACTIVO
$params = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $aqui 'verificar.ps1'), '-Clase', $clase, '-Accion', $cmd)
if ($plan) { $params += @('-Plan', $plan) }
if ($env:VEREDICTOS_LOG) { $params += @('-Registro', $env:VEREDICTOS_LOG) }
$salida = & powershell.exe @params 2>&1 | Out-String
$codigo = $LASTEXITCODE
$salida = $salida.Trim()

switch ($codigo) {
  0 { exit 0 }
  1 { Responder 'deny' ("Verificador: " + $salida) }
  2 { Responder 'ask' ("Verificador pide revisión: " + $salida) }
  default {
    if ($destructiva) { Responder 'deny' ("Verificador sin respuesta y la acción es destructiva: no se ejecuta. " + $salida) }
    else { Responder 'allow' ("Verificador sin respuesta; acción no destructiva. Registrar el fallo en la evidencia del plan. " + $salida) }
  }
}
