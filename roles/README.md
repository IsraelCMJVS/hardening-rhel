# rhel_cis_hardening

Role de Ansible para evaluar y remediar hardening CIS Level 1 en RHEL 8 y RHEL 9 usando OpenSCAP.

## Modos de operación
- `scan_only`
- `scan_and_remediate`

## Paquetes requeridos
- openscap
- openscap-scanner
- scap-security-guide

## Reportes generados
- Pre-scan XML/HTML
- Remediation XML/HTML
- Post-scan XML/HTML
- Remediation log HTML
- Summary report HTML

## Variables principales
- `hardening_mode`
- `hardening_minimum_score`
- `hardening_scap_profile`
- `hardening_bastion_base_dir`
- `hardening_remove_prereqs_at_end`

## Notas
- El datastream de RHEL 9 debe validarse en el ambiente destino.
- Algunos controles pueden quedar como manual, unknown o no aplicables.
- El role no obliga a 100% de cumplimiento.