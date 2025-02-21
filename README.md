# 📌 Trivia API - FastAPI

**Trivia API** es un sistema basado en **FastAPI** que permite a los usuarios participar en trivias, responder preguntas y obtener puntuaciones. Los administradores pueden gestionar trivias, preguntas y asignar trivias a los usuarios. El administrador tambien puede ver el ranking de mejores jugadores y ver todas las estadisticas de un jugador

---

## 📚 Índice

1. [🛠️ Herramientas Necesarias](#-herramientas-necesarias)
2. [🚀 Levantar el Proyecto](#-levantar-el-proyecto)
3. [🔍 Probar la API](#-probar-la-api)
4. [📌 Endpoints](#-endpoints)
5. [🛠️ Modelado de Base de Datos](#-modelado-de-base-de-datos)
6. [👨‍💻 Tecnologías Usadas](#-tecnolog%C3%ADas-usadas)

---

## 🛠️ Herramientas Necesarias

Para ejecutar este proyecto, necesitas:

- 🐳 **Docker** (para contenedores y base de datos)
- 🏗️ **Docker Compose** (para orquestar los servicios)
- 📝 **Editor de Código** (VS Code, PyCharm o similar)
- 🖥️ **Git** (para clonar el repositorio)
- 🔄 **Postman** o **cURL** (para probar la API)
- 🛠️ **Extensiones Recomendadas en VS Code**:
  - 🐍 Python
  - 📦 Docker
  - 🔗 GitLens

---

## 🚀 Levantar el Proyecto

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/eliasyusti/talatrivia-prueba.git
cd talatrivia-prueba
```

### 2️⃣ Levantar los Contenedores

Desde la raíz del proyecto, ejecuta:

```bash
docker-compose up --build
```

Esto creará la base de datos, ejecutará las migraciones y agregará datos iniciales.

### 🔐 Credenciales Iniciales

El sistema ya cuenta con un usuario **Admin** preconfigurado:

- **Email:** `admin@example.com`
- **Contraseña:** `admin123`

Puedes usar estas credenciales para iniciar sesión y gestionar usuarios.

---

## 🔍 Probar la API

Puedes probar los endpoints de la API de dos maneras:

1. **Swagger UI de FASTAPI**: Accediendo a `http://localhost:8086/docs#/`. Necesitas autenticación en **Authorize** con las credenciales preconfiguradas.
2. **Postman**: Usando la colección de Postman **API-TALANA-TRIVIA.postman_collection.json** incluida en el repositorio.

🚀🚀🚀 La mayoría de los endpoints requieren autenticación mediante token.

---

## 📌 Endpoints

A continuación, se detallan los principales endpoints del sistema.

### 🔹 **Autenticación**

| Método | Endpoint      | Descripción                           |
| ------ | ------------- | ------------------------------------- |
| `POST` | `/auth/login` | 🔑 Genera un token de acceso (Login). |

### 🔹 **Gestión de Usuarios (Solo Admins)**

| Método   | Endpoint                                               | Descripción                                |
| -------- | ------------------------------------------------------ | ------------------------------------------ |
| `POST`   | `/admin/gestion_usuarios/crear_usuario_admin`          | 👤 Crea un usuario (Admin o User).         |
| `GET`    | `/admin/gestion_usuarios/listar_usuarios`              | 📜 Lista todos los usuarios con sus roles. |
| `GET`    | `/admin/gestion_usuarios/usuario_by_id/{user_id}`      | 🔍 Obtiene un usuario por su ID.           |
| `PUT`    | `/admin/gestion_usuarios/actualizar_usuario/{user_id}` | ✏️ Actualiza los datos de un usuario.      |
| `DELETE` | `/admin/gestion_usuarios/eliminar_usuario/{user_id}`   | 🗑️ Elimina un usuario.                     |

### 🔹 **Gestión de Trivias (Solo Admins)**

| Método   | Endpoint                        | Descripción                       |
| -------- | ------------------------------- | --------------------------------- |
| `POST`   | `/admin/trivias/`               | 🆕 Crea una trivia sin preguntas. |
| `POST`   | `/admin/trivias/with-questions` | 🆕 Crea una trivia con preguntas. |
| `PUT`    | `/admin/trivias/{trivia_id}`    | ✏️ Actualiza una trivia.          |
| `DELETE` | `/admin/trivias/{trivia_id}`    | 🗑️ Elimina una trivia.            |
| `GET`    | `/admin/trivias/`               | 📜 Lista todas las trivias.       |
| `GET`    | `/admin/trivias/{trivia_id}`    | 🔍 Obtiene una trivia por ID.     |

### 🔹 **Asignación de Trivias a Usuarios (Solo Admins)**

| Método | Endpoint                              | Descripción                                  |
| ------ | ------------------------------------- | -------------------------------------------- |
| `POST` | `/user_trivia/admin/asignar_trivias`  | 🎯 Asigna trivias a un usuario.              |
| `GET`  | `/user_trivia/user/trivias/{user_id}` | 📜 Lista las trivias asignadas a un usuario. |
| `GET`  | `/user_trivia/admin/users_trivias`    | 📜 Lista usuarios con sus trivias asignadas. |

### 🔹 **Realización de Trivias (Usuarios)**

| Método | Endpoint                              | Descripción                        |
| ------ | ------------------------------------- | ---------------------------------- |
| `POST` | `/users/realizar_trivia/{trivia_id}/` | 📝 Un usuario responde una trivia. |

### 🔹 **Estadísticas (Solo Admins)**

| Método | Endpoint                                    | Descripción                                           |
| ------ | ------------------------------------------- | ----------------------------------------------------- |
| `GET`  | `/admin/estadisticas/rendimiento/{user_id}` | 📊 Obtiene el rendimiento del usuario en sus trivias. |
| `GET`  | `/admin/estadisticas/ranking`               | 🏆 Lista los usuarios con mejor puntuación.           |

---

## 🛠️ Modelado de Base de Datos

El modelo de datos está diseñado para manejar usuarios, trivias y respuestas con relaciones bien definidas. A continuación, se explica cada entidad y sus relaciones:

1. **Usuarios (`users`)**

   - Contiene información sobre los usuarios.
   - Relación uno a muchos con `user_trivias` (historial de trivias realizadas).
   - Relación uno a muchos con `user_answers` (respuestas a preguntas).

2. **Roles (`roles`)**

   - Define los roles de usuario (`Admin`, `User`).
   - Relación uno a muchos con `users`.

3. **Trivias (`trivias`)**

   - Contiene las trivias disponibles.
   - Relación muchos a muchos con `questions` (preguntas asignadas a una trivia).

4. **Preguntas (`questions`)**

   - Contiene las preguntas de las trivias.
   - Relación muchos a muchos con `trivias`.
   - Relación uno a muchos con `options` (posibles respuestas a la pregunta).

5. **Opciones (`options`)**

   - Respuestas posibles para una pregunta.
   - Relación uno a muchos con `questions`.

6. **Respuestas de Usuarios (`user_answers`)**

   - Almacena las respuestas seleccionadas por los usuarios.
   - Relación uno a muchos con `users` y `trivias`.

7. **Historial de Trivia (`user_trivias`)**

   - Almacena el historial de trivias completadas por cada usuario.
   - Contiene la puntuación y respuestas correctas/incorrectas.

8. **Asignación de Trivias (`user_trivia_assignments`)**
   - Relación que asigna qué trivias puede realizar un usuario.
   - Relación uno a muchos con `users` y `trivias`.

Este modelado permite una gestión eficiente de trivias, respuestas y puntuaciones.

---

## 👨‍💻 Tecnologías Usadas

- 🐍 **Python 3.11**
- ⚡ **FastAPI** (Framework principal)
- 🛢️ **PostgreSQL** (Base de datos)
- 🏗️ **SQLAlchemy** (ORM)
- 🔑 **JWT** (Autenticación)
- 🐳 **Docker** (Para despliegue y ejecución)

---

## 📞 Contacto

Si tienes dudas o sugerencias, contáctame en [eliasyusti@gmail.com](mailto:eliasyusti@gmail.com). 🚀
