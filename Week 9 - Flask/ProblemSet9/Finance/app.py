import re
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import apology, login_required, lookup, usd, get_time, check_password
from flask_session import Session


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks."""

    user_id = session["user_id"]
    portfolio = db.execute("SELECT * FROM portfolios WHERE user_id = ?", user_id)
    cash_left = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    # Getting the amount of cash the user has left to spend
    if cash_left and "cash" in cash_left[0]:
        cash_left = float(cash_left[0]["cash"])
    else:
        cash_left = 0.0

    total_amount = cash_left

    # Updating the current price and the overall stock value for each stock to be displayed in real time
    try:
        for stock in portfolio:
            symbol = stock["symbol"]
            stock_info = lookup(symbol)

            current_price = float(stock_info["price"])
            stock_value = current_price * stock["shares"]

            stock.update({"current_price": current_price, "stock_value": stock_value})
            total_amount += float(stock["stock_value"])
    except (ValueError, LookupError):
        return apology("Failed to update stock prices!")

    return render_template(
        "index.html",
        portfolio=portfolio,
        cash_left=cash_left,
        total_amount=total_amount,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user_id = session["user_id"]

        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        shares = request.form.get("shares")

        # Checking for symbol to be valid
        if not symbol or not stock:
            return apology("Symbol is not valid!")

        # Checking for shares number to be positive
        if not shares.isdigit():
            return apology("Number of shares must be a positive digit!")

        transaction_value = int(shares) * stock["price"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash[0]["cash"]

        # Making sure user has enough cash to buy the shares
        if user_cash < transaction_value + 1:
            return apology("Not enough money!", 401)

        # Perform the aquisition and update database
        update_user_cash = user_cash - transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_user_cash, user_id)

        # Format balance
        balance = f"${update_user_cash:,.2f} (-${transaction_value:,.2f})"

        # Add transaction to portfolio database
        db.execute(
            "INSERT INTO portfolios (user_id, name, symbol, shares, paid_price, current_price, date, stock_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            user_id,
            stock["name"],
            symbol,
            shares,
            stock["price"],
            stock["price"],
            get_time(),
            stock["price"],
        )

        # Add transaction to history database
        db.execute(
            "INSERT INTO history (user_id, name, symbol, shares, action, balance, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            user_id,
            stock["name"],
            symbol,
            shares,
            "BOUGHT",
            balance,
            get_time(),
        )

        flash(f"Successfully bought {shares} shares of {symbol}!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    user_id = session["user_id"]
    portfolio = db.execute("SELECT * FROM history WHERE user_id = ?", user_id)

    return render_template("history.html", portfolio=portfolio)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username!", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Must provide password!", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Search details about the stock
        stock = lookup(str(request.form.get("symbol")))

        # Check for empty field
        if not stock:
            return apology("Invalid symbol!")

        # Format price
        stock["price"] = usd(stock["price"])

        return render_template("quoted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for empty fields
        if any(not field for field in [username, password, confirmation]):
            return apology("Fields cannot be empty!")

        # Ensure username is at least 4 characters long
        if len(username) < 4:
            return apology("Username must be at least 4 characters long!", 403)

        # Ensure username consists only of characters and digits
        if not username.isalnum():
            return apology("Username must contain only characters and digits!", 403)

        # Ensure password is stronger (has characters, digits, symbols)
        if len(password) < 8:
            return apology("Password must be at least 8 characters long!", 403)
        if (
            not re.search("[a-zA-Z]", password)
            or not re.search("[0-9]", password)
            or not re.search("[!@#$%^&*()]", password)
        ):
            return apology("Password must contain characters, digits and symbols!", 403)

        # Check for password to be the same
        if password != confirmation:
            return apology("Passwords do not match!", 400)

        # Make sure the name isn't registered already or the field is empty
        if len(db.execute("SELECT * FROM users WHERE username = ?", username)) > 0:
            return apology("Username already taken!", 400)

        # Hash password
        hashed_password = generate_password_hash(password)
        # Add username & hashed password in the database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            hashed_password,
        )

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    user_id = session["user_id"]
    portfolio = db.execute("SELECT * FROM portfolios WHERE user_id = ?", user_id)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        shares = int(request.form.get("shares"))

        owned_stock = db.execute(
            "SELECT shares FROM portfolios WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol,
        )

        # Check if user owns shares of the stock
        if not owned_stock:
            return apology(f"You don't own any shares of {symbol}!")

        # Check if user has enough shares to sell
        current_shares = sum([stock["shares"] for stock in owned_stock])
        if current_shares < shares:
            return apology("You don't have enough shares to sell!")

        # Retrieve user's balance
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash[0]["cash"]
        # Deposit value of sold shares
        current_price = stock["price"]
        cash += shares * current_price

        # Perform the sale
        for info in owned_stock:
            # Update database if user sells less shares than the total amount he owns
            if info["shares"] > shares:
                db.execute(
                    "UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?",
                    info["shares"] - shares,
                    user_id,
                    symbol,
                )
            # Delete stock from portfolio if all shares were sold
            else:
                db.execute(
                    "DELETE FROM portfolios WHERE user_id = ? AND symbol = ?",
                    user_id,
                    symbol,
                )

        # Format balance
        balance = f"${cash:,.2f} (+${(shares * current_price):,.2f})"

        # Update user's cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)

        # Add transaction to history database
        db.execute(
            "INSERT INTO history (user_id, name, symbol, shares, action, balance, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            user_id,
            stock["name"],
            symbol,
            shares,
            "SOLD",
            balance,
            get_time(),
        )

        flash(f"Successfully sold {shares} shares of {symbol}!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("sell.html", portfolio=portfolio)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit funds to account."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user_id = session["user_id"]

        amount = int(request.form.get("sum"))
        account = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure password is correct
        check_password(account[0]["hash"], request.form.get("password"))

        # Add funds to account
        cash = account[0]["cash"] + amount
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)

        flash(f"Successfully added ${amount} to your balance!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("deposit.html")


@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    """Withdraw funds from account."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user_id = session["user_id"]

        amount = int(request.form.get("sum"))
        account = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure password is correct
        check_password(account[0]["hash"], request.form.get("password"))

        # Ensure user cannot withdraw more than left cash
        if amount > account[0]["cash"]:
            return apology("Cannot withdraw more than cash left!")

        # Withdraw funds from account
        cash = account[0]["cash"] - amount
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)

        flash(f"Successfully withdrew ${amount} from your balance!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("withdraw.html")
