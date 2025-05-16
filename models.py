from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///livro.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Livro(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(40), nullable=False, index=True)
    autor = Column(String(40), nullable=False, index=True)
    descricao = Column(String(40), nullable=False, index=True)
    categoria = Column(String(40), nullable=False, index=True)


    def __repr__(self):
        return '<Livros: Titulo: {} Autor: {}>'.format(self.titulo, self.autor)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_user(self):
        dados_livros = {
            'id': self.id,
            'Titulo': self.titulo,
            'Autor': self.autor,
            'Categoria': self.categoria,
            'Descrição': self.descricao,
        }

        return dados_livros


class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False, index=True)
    cargo = Column(String(40), nullable=False, index=True)
    salario = Column(String(40), nullable=False, index=True)



    def __repr__(self):
        return '<Funcionarios: Cargo: {} Salario: {}>'.format(self.cargo, self.salario)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_user(self):
        dados_livros = {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
            'salario': self.salario,
        }

        return dados_livros


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()