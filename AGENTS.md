# Contexto del proyecto

Este proyecto compara listas de cartas de Magic: The Gathering para encontrar cartas buscadas que están disponibles para comprar.

- La documentación y los mensajes visibles están en español.
- Los identificadores, módulos y nombres de configuración están en inglés.
- Las URLs de entrada están en `config/wanted-card-lists.yaml` y `config/sale-card-lists.yaml`.
- Los resultados locales están en `output/` y no se versionan.
- Cada plataforma debe tener su propio adaptador dentro de `src/sources/`.
