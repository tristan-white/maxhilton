import os
from sqlalchemy import create_engine, text, Table, Column, Integer, MetaData, String, Date, Numeric
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# commit as you go
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()

# begin once
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )

# Fetching rows
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))

    for row in result:
        print(f"x: {row.x}, y: {row.y}")

    for dict_row in result.mappings():
        x = dict_row["x"]
        y = dict_row["y"]
        print(f"x: {x}, y: {y}")

metadata_obj = MetaData()

prices_table = Table(
    "prices",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("hotel_code", String, nullable=False),
    Column("date", Date, nullable=False),
    Column("price", Numeric, nullable=False),
)

metadata_obj.create_all(engine)

class Base(DeclarativeBase):
    pass

class HotelPrice(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_code: Mapped[str] = mapped_column(String(10))
    date: Mapped[str] = mapped_column(String(10))
    rate: Mapped[int] = mapped_column(Numeric(10, 2))

    def __repr__(self) -> str:
        return f"HotelPrice({self.id!r}, {self.hotel_code!r}, {self.date!r}, {self.rate!r})"

hp = HotelPrice(hotel_code="yqbmthw", date=date(2025, 1, 11), rate=100.00)

Base.metadata.create_all(engine)


with Session(engine) as session:
    session.add(hp)
    session.commit()

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM prices"))
    for row in result:
        print(f"id: {row.id}, hotel_code: {row.hotel_code}, date: {row.date}, price: {row.price}")