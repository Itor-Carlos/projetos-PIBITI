import mysql.connector
from enum import Enum
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
import logging

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

def get_categoria(valor):
    for cat in Categoria:
        if cat.value == valor:
            return cat
    return None

class Transacao:
    def __init__(self, tipo: Tipo, categoria: Categoria, valor: float, descricao: str, data: str):
        self.tipo = tipo
        self.categoria = categoria
        self.valor = valor
        self.descricao = descricao
        self.data = data

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="calculadora_financeira"
    )



@mcp.tool()
async def inserir_transacao(type: Tipo, category: Categoria, amount: float, description: str, date: str):
    try:
        """
        Inserting a financial transaction into the database.
        Args:
            type: Transaction type (Income or Expense)
            category: Transaction category (e.g. Food, Transportation)
            amount: Transaction amount
            description: Transaction description
            date: Transaction date (YYYY-MM-DD)
        Returns:
            A dict indicating success or failure.
        """

        connection = get_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO transacao (tipo, categoria, valor, descricao, data) VALUES (%s, %s, %s, %s, %s)"
        values = (type.value, category.value, amount, description, date)
        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        connection.close()
        logging.info("Transação inserida com sucesso: %s", values)
        return {"status": "ok"}
    except Exception as e:
        logging.exception("Erro ao inserir transação")
        return {"status": "erro", "detalhe": str(e)}


@mcp.tool()
async def get_by_descricao(descricao: str):
    """
    Fetch all financial transactions from the database filtered by description.
    
    Args:
        descricao (str): Description filter for transactions
    """
    try:
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM transacao WHERE descricao LIKE %s"
            cursor.execute(sql, (f"%{descricao}%",))
            results = cursor.fetchall()
        connection.close()
        logging.info("Transações recuperadas com sucesso")
        return results
    except Exception as e:
        logging.exception("Erro ao recuperar transações")
        return {"status": "erro", "detalhe": str(e)}

@mcp.tool()
async def transacao_mes_ano(mes: int, ano: int):
    """
    Fetch all financial transactions from the database filtered by month and year.
    
    Args:
        mes (int): Month filter for transactions (1-12)
        ano (int): Year filter for transactions (e.g., 2023)
    
    Returns:
        list[dict]: A list of transactions.
    """
    try:
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM transacao WHERE MONTH(data) = %s AND YEAR(data) = %s"
            cursor.execute(sql, (mes, ano))
            results = cursor.fetchall()
        connection.close()
        logging.info("Transações recuperadas com sucesso")
        return results
    except Exception as e:
        logging.exception("Erro ao recuperar transações")
        return {"status": "erro", "detalhe": str(e)}

from enum import Enum

@mcp.tool()
async def get_resume_by_categoria(categoria: str):
    """
        Fetch all financial transaction from database filtered by categoria
        
        Args:
            categoria (str): Categoria filter for transactions (ex: Alimentação, Lazer)
        
        Returns:
            list[dict]: Lista de dicionários, onde cada item contém:
                - "tipo" (str): tipo da transação.
                - "total" (float): soma dos valores agrupados por tipo.
    """
    try:
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = """
                SELECT SUM(valor) AS total, tipo
                FROM transacao
                WHERE categoria = %s
                GROUP BY tipo;
            """
            
            category = get_categoria(categoria)
            if category is None:
                raise ValueError(f"Categoria inválida: {categoria}")

            cursor.execute(sql, (category.value,))
            results = cursor.fetchall()

        connection.close()
        return results
    
    except Exception as exception:
        return {"status": "erro", "detalhe": str(exception)}

@mcp.tool()
async def get_transacoes(date: str):
    """
    Fetch all financial transactions from the database filtered by date.
    
    Args:
        date (str): Date filter for transactions (YYYY-MM-DD)

    Returns:
        list[dict]: A list of transactions.
    """
    try:
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM transacao WHERE data = %s"
            cursor.execute(sql, (date))
            results = cursor.fetchall()
        connection.close()
        logging.info("Transações recuperadas com sucesso")
        return results
    except Exception as e:
        logging.exception("Erro ao recuperar transações")
        return {"status": "erro", "detalhe": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")