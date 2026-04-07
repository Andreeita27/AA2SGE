# FASE 1: Análisis y Modelado de Datos
# 1.1 Justificación del Modelo de Datos

El modelo está organizado en dos tipos de entidades: Maestros y Transaccionales, siguiendo la estructura típica de un MiniERP.

- Entidades Maestras:

Son los datos base del sistema, relativamente estables y que no dependen de otras entidades:

    - Cliente (core): Contiene información identificativa del cliente (NIF, nombre, email). Referenciada por los pedidos.
    - Producto (core): Incluye SKU, nombre y precio base del catálogo. Referenciado por las líneas de pedido.
    - Estado (core): Tabla de estados de un pedido (Ej: Pendiente, Enviado, Completado…)Referenciada por cada pedido.

- Entidades Transaccionales:

Representan operaciones o movimientos dentro del sistema:

    - Pedido (ventas): Contiene datos de la operación comercial: cliente, fecha, estado.
    - LineaPedido (ventas): Representa cada producto incluido en un pedido, con cantidad y precio unitario. Tiene una constraint que obliga a que la cantidad sea mayor que cero.

- Relaciones y Cardinalidades

El modelo está basado en las siguientes relaciones:

* Ciente - Pedido

Un Cliente puede tener N Pedidos.
Un Pedido pertenece a un único Cliente.

Implementado mediante ForeignKey(Cliente, on_delete=RESTRICT) en Pedido.

* Pedido - LíneaPedido

Un Pedido tiene N Líneas de Pedido.
Cada LíneaPedido pertenece a un único Pedido.

Implementado con ForeignKey(Pedido, related_name='lineas').

* Producto - LíneaPedido

Un Producto puede estar en N Líneas de Pedido distintas.
Cada LíneaPedido referencia un único Producto.

Implementado con ForeignKey(Producto, on_delete=RESTRICT).

* Estado → Pedido

Un Estado puede aplicarse a muchos pedidos.
Cada Pedido tiene un estado único.

Implementado con ForeignKey(Estado, on_delete=PROTECT).

# 1.2 Diagrama Entidad–Relación (ER)

CLIENTE {
    int id PK
    string nif
    string nombre
    string email
}

PRODUCTO {
    int id PK
    string sku
    string nombre
    decimal precio
}

ESTADO {
    int id PK
    string nombre
}

PEDIDO {
    int id PK
    datetime fecha_creacion
    int cliente_id FK
    int estado_id FK
}

LINEAPEDIDO {
    int id PK
    int pedido_id FK
    int producto_id FK
    int cantidad
    decimal precio_unitario
}

CLIENTE ||--o{ PEDIDO : "tiene"
ESTADO ||--o{ PEDIDO : "define"
PEDIDO ||--o{ LINEAPEDIDO : "incluye"
PRODUCTO ||--o{ LINEAPEDIDO : "aparece en"

## AA2 - KPI CRM: Tasa de Conversión

La tasa de conversión mide el porcentaje de oportunidades comerciales que terminan convirtiéndose en una venta cerrada con éxito.

### Fórmula

Tasa de Conversión = (Oportunidades Ganadas / Total de Oportunidades) * 100

### Cómo se calcula en este proyecto

Para calcular este KPI se utilizan los datos del modelo `Oportunidad`:

- Se cuentan todas las oportunidades registradas.
- Se cuentan cuántas tienen la etapa `Cerrada Ganada`.
- Se divide el número de oportunidades ganadas entre el total.
- El resultado se multiplica por 100 para obtener el porcentaje.

### Ejemplo

Si existen 10 oportunidades en total y 4 están marcadas como `Cerrada Ganada`, la tasa de conversión será:

(4 / 10) * 100 = 40%