from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(250), nullable=False)
    apellido: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    fecha_de_subscripcion: Mapped[str] = mapped_column(String(50), nullable=True) 
    
    # Relación: Un usuario tiene muchos favoritos
    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido
            # No serializamos el password por seguridad
        }

class Personaje(db.Model):
    __tablename__ = 'personaje'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(250), nullable=False)
    ano_de_nacimiento: Mapped[str] = mapped_column(String(250), nullable=True)
    genero: Mapped[str] = mapped_column(String(250), nullable=True)
    altura: Mapped[str] = mapped_column(String(250), nullable=True)
    color_de_cabello: Mapped[str] = mapped_column(String(250), nullable=True)
    color_de_ojos: Mapped[str] = mapped_column(String(250), nullable=True)
    
    # Relación Inversa
    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ano_de_nacimiento": self.ano_de_nacimiento
        }

class Planeta(db.Model):
    __tablename__ = 'planeta'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(250), nullable=False)
    clima: Mapped[str] = mapped_column(String(250), nullable=True)
    poblacion: Mapped[str] = mapped_column(String(250), nullable=True)
    periodo_orbital: Mapped[str] = mapped_column(String(250), nullable=True)
    periodo_de_rotacion: Mapped[str] = mapped_column(String(250), nullable=True)
    diametro: Mapped[str] = mapped_column(String(250), nullable=True)

    # Relación Inversa
    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima
        }

class Favorito(db.Model):
    __tablename__ = 'favorito'
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Claves foráneas (Foreign Keys)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey('personaje.id'), nullable=True)
    planeta_id: Mapped[int] = mapped_column(ForeignKey('planeta.id'), nullable=True)
    
    # Relaciones
    usuario: Mapped["Usuario"] = relationship(back_populates="favoritos")
    personaje: Mapped["Personaje"] = relationship(back_populates="favoritos")
    planeta: Mapped["Planeta"] = relationship(back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personaje_id": self.personaje_id,
            "planeta_id": self.planeta_id
        }
