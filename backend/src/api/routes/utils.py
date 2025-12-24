from fastapi import HTTPException, status
from psycopg import Connection


def get_user_or_404(conn: Connection, user_id: int) -> dict:
    """Get user by ID or raise 404."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return row


def get_problem_or_404(conn: Connection, problem_id: int) -> dict:
    """Get problem by ID or raise 404."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM problems WHERE problem_id = %s", (problem_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")
    return row


def get_problem_with_author(conn: Connection, problem_id: int) -> dict:
    """Get problem with author information (joined) or raise 404."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                p.problem_id,
                p.user_id,
                p.title,
                p.description,
                p.problem_type,
                p.created_at,
                p.resolved,
                u.user_id as author_user_id,
                u.username as author_username,
                u.email as author_email,
                u.first_name as author_first_name,
                u.last_name as author_last_name,
                u.created_at as author_created_at
            FROM problems p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.problem_id = %s
            """,
            (problem_id,),
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")

    # Restructure to nested format for ProblemWithAuthor schema
    return {
        "problem_id": row["problem_id"],
        "user_id": row["user_id"],
        "title": row["title"],
        "description": row["description"],
        "problem_type": row["problem_type"],
        "created_at": row["created_at"],
        "resolved": row["resolved"],
        "author": {
            "user_id": row["author_user_id"],
            "username": row["author_username"],
            "email": row["author_email"],
            "first_name": row["author_first_name"],
            "last_name": row["author_last_name"],
            "created_at": row["author_created_at"],
        },
    }


def get_solution_or_404(conn: Connection, solution_id: int) -> dict:
    """Get solution by ID or raise 404."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM solutions WHERE solution_id = %s", (solution_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solution not found")
    return row


def get_resource_or_404(conn: Connection, resource_id: int) -> dict:
    """Get resource by ID or raise 404."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM resources WHERE resource_id = %s", (resource_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return row


def get_tag_or_404(conn: Connection, tag_id: int) -> dict:
    """Get tag by ID or raise 404."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tags WHERE tag_id = %s", (tag_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return row
