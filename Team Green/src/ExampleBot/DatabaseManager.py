import sqlite3
from datetime import datetime

class DatabaseManager:
  def __init__(self):
    self.conn = sqlite3.connect("inventory.db")
    self.create_tables()
    self.conn.commit()
    #self.conn.close()

  def create_tables(self):
    """ Creates the tables in the inventory database.
    """
    item_table = """CREATE TABLE IF NOT EXISTS Items (
      ItemID Integer PRIMARY KEY AUTOINCREMENT,
      ItemName varchar(255),
      ItemDescription varchar(255),
      ItemAmount int
    );"""

    transaction_table = """CREATE TABLE IF NOT EXISTS Transactions (
      ItemID int,
      User int,
      TakenAmount varchar(255),
      TakenDate datetime,
      PRIMARY KEY (ItemID, User, TakenDate),
      FOREIGN KEY(ItemID) REFERENCES Items(ItemID)
    );"""

    self.conn.execute(item_table)
    self.conn.execute(transaction_table)

  def get_item_names(self):
    """
    Gets list of all item names in the Items table
    :return:
    """
    with self.conn:
      sql_select_item_names = """
      SELECT ItemName FROM Items;
      """
      cur = self.conn.cursor()
      cur.execute(sql_select_item_names)
      value = [row[0] for row in cur]
      #cur.close()
    # self.conn.close()
    return value

  def get_item_description(self, item_name):
    """Gets the description of an item in the database
    :param item_name: Name of the item
    :return: Description of the item in the database
    """
    with self.conn:
      cur = self.conn.cursor()
      cur.execute("""
      SELECT ItemDescription FROM Items
      WHERE Items.ItemName = ?
       """, (item_name,))
      description = cur.fetchone()[0]
      #cur.close()
    # self.conn.close()
    return description

  def get_item_amount(self, item_name):
    """Gets the amount of an item in the database
    :param item_name: Name of the item
    :return: Amount in the database
    """
    with self.conn:
      cur = self.conn.cursor()
      cur.execute("""
      SELECT ItemAmount FROM Items
      WHERE Items.ItemName = ?
       """, (item_name,))
      amount = cur.fetchone()[0]
      #cur.close()
    # self.conn.close()
    return amount

  def add_item(self, item_name, item_description, item_amount: int):
    """Adds an item to the database.
    :param item_name: Name of the item being added
    :param item_description: Description of the item being added
    :param item_amount: The total number of items that can be taken
    :return:
    """
    with self.conn:
      self.conn.execute("INSERT INTO Items (ItemName, ItemDescription, ItemAmount) VALUES (?, ?, ?);", (item_name, item_description, item_amount))
    # self.conn.close()

  def add_item_take_record(self, item_name, taken_amount, user):
    """Adds a record to table Transactions
    :param item_name: Name of item that was taken
    :param taken_amount: Amount of that item that was taken
    :param user: User which took the item
    :return:
    """
    taken_date = datetime.now()
    with self.conn:
      #self.conn.execute("INSERT INTO Transactions (ItemID, User, TakenAmount, TakenDate) VALUES (?, ?, ?, ?)", (item_id, user, taken_amount, taken_date))
      self.conn.execute("""
      INSERT INTO Transactions (ItemId, User, TakenAmount, TakenDate)
      VALUES 
      ((SELECT ItemId FROM Items WHERE ItemName = ?), ?, ?, ?)
      """, (item_name, user, taken_amount, taken_date)) 
    #self.conn.close()

  def update_item_amount(self, item_name: str, new_amount:int):
    """Updates the item amount in the database
    :param item_name: Name of the item being decremented/incremented
    :param new_amount: The new total of the item in stock
    return: 
    """
    with self.conn:
      self.conn.execute("""
      UPDATE Items
      SET 
        ItemAmount = ?
      WHERE
        ItemName = ?;
      """, (new_amount, item_name))
    #self.conn.close

  def return_item(self):
    pass

