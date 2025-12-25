# データベース構造（MVP）

## ER図

```mermaid
erDiagram
    USER {
        int id PK
        string nickname
        datetime created_at
    }

    CONSULTATION {
        int id PK
        int user_id FK
        string summary
        string status
        datetime created_at
    }

    MESSAGE {
        int id PK
        int consultation_id FK
        string sender_type
        text content
        datetime sent_at
    }

    RESERVATION {
        int id PK
        int consultation_id FK
        datetime start_time
        datetime end_time
        string status
    }

    USER ||--o{ CONSULTATION : submits
    CONSULTATION ||--o{ MESSAGE : has
    CONSULTATION ||--o{ RESERVATION : schedules