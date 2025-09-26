import logging
from enum import Enum
from typing import List, Dict, Union, Optional
from datetime import datetime

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP("calculadora_financeira")

class Tipo(Enum):
    RECEITA = "Receita"
    DESPESA = "Despesa"


class Categoria(Enum):
    ALIMENTACAO = "Alimentação"
    TRANSPORTE = "Transporte"
    MORADIA = "Moradia"
    LAZER = "Lazer"
    SAUDE = "Saúde"
    EDUCACAO = "Educação"
    OUTROS = "Outros"


def get_connection() -> MySQLConnection:
    """Create a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="calculadora_financeira"
    )


class DB:
    """Helper class to automatically manage MySQL connections."""

    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()


def get_categoria(valor: str) -> Optional[Categoria]:
    """Convert a string into a Categoria enum if valid, otherwise return None."""
    try:
        return Categoria(valor.capitalize())
    except ValueError:
        return None


@mcp.tool()
def inserir_transacao(tipo: Tipo, categoria: Categoria, valor: float, descricao: str, data: str) -> Dict[str, str]:
    """
    Insert a financial transaction into the database.

    Args:
        tipo (Tipo): Transaction type (Receita or Despesa).
        categoria (Categoria): Transaction category.
        valor (float): Transaction amount.
        descricao (str): Description of the transaction.
        data (str): Transaction date (YYYY-MM-DD).

    Returns:
        Dict[str, str]: Operation status.
    """
    try:
        with DB() as cursor:
            sql = """
                INSERT INTO transacao (tipo, categoria, valor, descricao, data)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (tipo.value, categoria.value, valor, descricao, data))
        logging.info(f"Transaction inserted: {descricao} - {valor}")
        return {"status": "ok"}
    except Exception as e:
        logging.exception("Error inserting transaction")
        return {"status": "error", "details": str(e)}


@mcp.tool()
def get_transacoes_by_periodo(startData: str, finalData: str, categoria: Optional[Categoria] = None) -> List[Dict]:
    """
    Retrieve all transactions within a date range, with optional category filtering.

    Args:
        startData (str): Start date (YYYY-MM-DD).
        finalData (str): End date (YYYY-MM-DD).
        categoria (Categoria, optional): Category to filter.

    Returns:
        List[Dict]: List of transactions within the specified range.
    """
    try:
        with DB() as cursor:
            sql = """
                SELECT *
                FROM transacao
                WHERE data BETWEEN %s AND %s
            """
            params = [startData, finalData]

            if categoria:
                sql += " AND categoria = %s"
                params.append(categoria.value)

            cursor.execute(sql, params)
            return cursor.fetchall()
    except Exception as exception:
        return [{
            "status": "error",
            "details": str(exception)
        }]


@mcp.tool()
def get_by_descricao(descricao: str) -> List[Dict]:
    """
    Search for transactions filtered by description.

    Args:
        descricao (str): Text to search within the description.

    Returns:
        List[Dict]: List of matching transactions.
    """
    try:
        with DB() as cursor:
            sql = "SELECT * FROM transacao WHERE descricao LIKE %s"
            cursor.execute(sql, (f"%{descricao}%",))
            return cursor.fetchall()
    except Exception as e:
        logging.exception("Error retrieving transactions")
        return [{"status": "error", "details": str(e)}]


@mcp.tool()
def transacao_mes_ano(mes: int, ano: int) -> List[Dict]:
    """
    Retrieve transactions filtered by month and year.

    Args:
        mes (int): Month number (1-12).
        ano (int): Year (YYYY).

    Returns:
        List[Dict]: List of transactions within the given month and year.
    """
    try:
        with DB() as cursor:
            sql = "SELECT * FROM transacao WHERE MONTH(data) = %s AND YEAR(data) = %s"
            cursor.execute(sql, (mes, ano))
            return cursor.fetchall()
    except Exception as e:
        logging.exception("Error retrieving transactions")
        return [{"status": "error", "details": str(e)}]


@mcp.tool()
def get_resume_by_categoria(categoria: str) -> List[Dict]:
    """
    Generate a summary of transactions grouped by type within a given category.

    Args:
        categoria (str): Category name.

    Returns:
        List[Dict]: List containing type and total amount grouped by type.
    """
    try:
        cat_enum = get_categoria(categoria)
        if cat_enum is None:
            raise ValueError(f"Invalid category: {categoria}")

        with DB() as cursor:
            sql = """
                SELECT tipo, SUM(valor) AS total
                FROM transacao
                WHERE categoria = %s
                GROUP BY tipo
            """
            cursor.execute(sql, (cat_enum.value,))
            return cursor.fetchall()
    except Exception as e:
        logging.exception("Error generating summary")
        return [{"status": "error", "details": str(e)}]


@mcp.tool()
def get_transacoes(date: str) -> List[Dict]:
    """
    Retrieve transactions for a specific date.

    Args:
        date (str): Transaction date (YYYY-MM-DD).

    Returns:
        List[Dict]: List of transactions found for the given date.
    """
    try:
        with DB() as cursor:
            sql = "SELECT * FROM transacao WHERE data = %s"
            cursor.execute(sql, (date,))
            return cursor.fetchall()
    except Exception as e:
        logging.exception("Error retrieving transactions")
        return [{"status": "error", "details": str(e)}]

@mcp.resource("resource://get_all_transacoes")
def get_all_transacoes() -> List[Dict]:
    """
    Retrieve all transactions from the database.

    Returns:
        List[Dict]: List of all transactions.
    """
    try:
        with DB() as cursor:
            sql = "SELECT * FROM transacao"
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        logging.exception("Error retrieving all transactions")
        return [{"status": "error", "details": str(e)}]

if __name__ == "__main__":
    mcp.run(transport="stdio")