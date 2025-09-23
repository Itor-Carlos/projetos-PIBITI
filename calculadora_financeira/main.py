import logging
from enum import Enum
from typing import List, Dict, Union
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
    """Cria conexão com o banco MySQL."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="calculadora_financeira"
    )


class DB:
    """Helper para gerenciar conexões automaticamente."""

    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()


def get_categoria(valor: str) -> Union[Categoria, None]:
    try:
        return Categoria(valor.capitalize())
    except ValueError:
        return None


@mcp.tool()
def inserir_transacao(tipo: Tipo, categoria: Categoria, valor: float, descricao: str, data: str
) -> Dict[str, str]:
    """
    Insere uma transação financeira no banco.
    """
    try:
        with DB() as cursor:
            sql = """
                INSERT INTO transacao (tipo, categoria, valor, descricao, data)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (tipo.value, categoria.value, valor, descricao, data))
        logging.info(f"Transação inserida: {descricao} - {valor}")
        return {"status": "ok"}
    except Exception as e:
        logging.exception("Erro ao inserir transação")
        return {"status": "erro", "detalhe": str(e)}


@mcp.tool()
def get_by_descricao(descricao: str) -> List[Dict]:
    """
    Busca transações filtradas pela descrição.
    """
    try:
        with DB() as cursor:
            sql = "SELECT * FROM transacao WHERE descricao LIKE %s"
            cursor.execute(sql, (f"%{descricao}%",))
            return cursor.fetchall()
    except Exception as e:
        logging.exception("Erro ao recuperar transações")
        return [{"status": "erro", "detalhe": str(e)}]


@mcp.tool()
def transacao_mes_ano(mes: int, ano: int) -> List[Dict]:
    """
    Busca transações filtradas por mês e ano.
    """
    try:
        with DB() as cursor:
            sql = "SELECT * FROM transacao WHERE MONTH(data) = %s AND YEAR(data) = %s"
            cursor.execute(sql, (mes, ano))
            return cursor.fetchall()
    except Exception as e:
        logging.exception("Erro ao recuperar transações")
        return [{"status": "erro", "detalhe": str(e)}]


@mcp.tool()
def get_resume_by_categoria(categoria: str) -> List[Dict]:
    """
    Resumo das transações agrupadas por tipo em uma categoria.
    """
    try:
        cat_enum = get_categoria(categoria)
        if cat_enum is None:
            raise ValueError(f"Categoria inválida: {categoria}")

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
        logging.exception("Erro ao gerar resumo")
        return [{"status": "erro", "detalhe": str(e)}]


@mcp.tool()
def get_transacoes(date: str) -> List[Dict]:
    """
    Busca transações por data exata (YYYY-MM-DD).
    """
    try:
        with DB() as cursor:
            sql = "SELECT * FROM transacao WHERE data = %s"
            cursor.execute(sql, (date,))
            return cursor.fetchall()
    except Exception as e:
        logging.exception("Erro ao recuperar transações")
        return [{"status": "erro", "detalhe": str(e)}]


if __name__ == "__main__":
    mcp.run(transport="stdio")