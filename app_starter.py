from flask import Flask, redirect, render_template, request, session, url_for, Response, send_file
import os
import io
import sqlite3 as sl
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = "tesla_amazon_stock.db"


@app.route("/")
def home():
    options = {
        "Tesla": "Tesla Stock",
        "Amazon": "Amazon Stock"
    }
    return render_template("home.html", locales=db_get_locales(), message="Please enter a date to search for.", options=options)


@app.route("/submit_locale", methods=["POST"])
def submit_locale():
    # session["locale"] = request.form["locale"].capitalize()
    session["locale"] = request.form["locale"]
    if 'locale' not in session or session["locale"] == "":
        return redirect(url_for("home"))
    if "data_request" not in request.form:
        return redirect(url_for("home"))
    session["data_request"] = request.form["data_request"]
    return redirect(url_for("locale_current", data_request=session["data_request"], locale=session["locale"]))


@app.route("/api/tech_stock/<data_request>/<locale>")
def locale_current(data_request, locale):
    return render_template("locale.html", data_request=data_request, locale=locale, project=False)


@app.route("/submit_projection", methods=["POST"])
def submit_projection():
    if 'locale' not in session:
        return redirect(url_for("home"))
    session["YEAR"] = request.form["YEAR"]
    # THESE NEED TO BE BACK IN!
    if session["locale"] == "" or session["data_request"] == "" or session["YEAR"] == "":
        return redirect(url_for("home"))
    return redirect(url_for("locale_projection", data_request=session["data_request"], locale=session["locale"]))


@app.route("/api/tech_stock/<data_request>/projection/<locale>")
def locale_projection(data_request, locale):
    return render_template("locale.html", data_request=data_request, locale=locale, project=True)


@app.route("/fig/<data_request>/<locale>")
def fig(data_request, locale):
    fig = create_figure(data_request, locale)

    # img = io.BytesIO()
    # fig.savefig(img, format='png')
    # img.seek(0)
    # w = FileWrapper(img)
    # # w = werkzeug.wsgi.wrap_file(img)
    # return Response(w, mimetype="text/plain", direct_passthrough=True)

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype="image/png")


def create_figure(data_request, year_):
    df = db_create_dataframe(data_request, year_)
    #df = pd.read_csv("csv_files/tesla.csv")
    print(session)

    if 'Date' not in session:
        conn = sl.connect(db)
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        fig.suptitle(data_request.capitalize() + " stock on " + year_)
        df = df[df["Open"].notnull()]
        query = "SELECT * FROM " + data_request + " WHERE YEAR = " + year_
        df_sql_query = pd.read_sql_query(query, conn)
        df = pd.DataFrame(df_sql_query)
        #print(df["Date"])
        df["YEAR"] = df["Date"].str[0:4]
        years_list = df["YEAR"].unique()
        grouped_years = df.groupby("YEAR")
        df["MONTH"] = df["Date"].str[5:7]
        month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for year in years_list:
            df_group = grouped_years.get_group(year)
            ax.plot(df_group["MONTH"], df_group["Open"],
                       label=year)
        #ax.plot(df["YEAR"], df["Open"])
        # ax.set(xlabel="date", ylabel="value")#, xticks=range(0, len(df), 31))

        xtickList = list(range(0, 12, 1))
        ax.xaxis.set_ticks(xtickList)
        ax.xaxis.set_ticklabels(month_list)
        ax.set(xlabel="Month", ylabel="Open")
        ax.legend()
        return fig
    else:
        # df['datemod'] = df['date'].map(datetime.datetime.toordinal)
        # y = df['cases'][-30:].values
        # X = df['datemod'][-30:].values.reshape(-1, 1)
        # # session['date'] = '11/11/20'  # REMOVE THIS LATER
        # dt = [[datetime.datetime.strptime(session['date'], '%m/%d/%y')]]
        # print('dt:', dt)
        # draw = datetime.datetime.toordinal(dt[0][0])
        # dord = datetime.datetime.fromordinal(int(draw))
        # regr = LinearRegression(fit_intercept=True, normalize=True, copy_X=True, n_jobs=2)
        # regr.fit(X, y)
        # pred = int(regr.predict([[draw]])[0])
        # df = df.append({'date': dord,
        #                 'value': pred,
        #                 'datemod': draw}, ignore_index=True)
        # fig = Figure()
        # ax = fig.add_subplot(1, 1, 1)
        # fig.suptitle('By ' + session['date'] + ', there will be ' + str(pred) + ' ' + data_request.capitalize() + " cases in " + date)
        # ax.plot(df["date"], df["value"])
        # ax.set(xlabel="date", ylabel="value")  # , xticks=range(0, len(df), 31))
        # return fig
        df['DATE_ORD'] = pd.to_datetime(df['DATE']) \
            .map(datetime.datetime.toordinal).dropna()
        print(df['DATE_ORD'].head(3))

        X_train, X_test, y_train, y_test = \
            train_test_split(df['DATE_ORD'], df['Open'],
                             test_size=0.5, random_state=0)

        # Models. Comment in and out as you see fit for your data.
        under_model = MLPClassifier(hidden_layer_sizes=(10, 10, 10),
                                    max_iter=1000)
        under_model = LinearRegression(fit_intercept=True,
                                       copy_X=True, n_jobs=2)
        model = make_pipeline(StandardScaler(with_mean=False),
                              under_model)
        #model = KNeighborsClassifier(n_neighbors=2)

        # print(X_train)
        # print(X_train.shape)
        # print(type(X_train))

        # Fit/Train your model and predict
        # Note these two lines are the same for all the models
        # due to the common API/interface of sklearn
        model.fit(X_train.values.reshape(-1, 1), y_train)
        y_pred = model.predict(X_test.values.reshape(-1, 1))
        # print(y_pred)
        # print(y_pred.shape)
        # print(type(y_pred))

        # Make a new dataframe to house and plot predictions
        df_pred = pd.DataFrame()
        df_pred['Predicted Open Price'] = y_pred
        df_pred['Observed Open Price'] = y_test
        df_pred['X_test'] = X_test
        df_pred = df_pred.dropna()  # get rid of NaNs

        # Convert back to original date strings from ordinal for graphing
        df_pred['DATE'] = df_pred['X_test'].astype(int) \
            .map(datetime.datetime.fromordinal)
        print(df_pred.head(3))
        # Plot Predicted y (Observed Temperature) vs Time
        df_pred.plot('DATE', 'Predicted Open Price', color='orange')
        plt.tight_layout()
        plt.show()


def db_create_dataframe(data_request, YEAR):
    conn = sl.connect(db)
    curs = conn.cursor()

    df = pd.DataFrame()


    table = data_request
    print(table)
    print(f'{table=}')
    # if locale.lower() == "us":
    #     locale = "US"
    print(f'{YEAR=}')
    stmt = "SELECT * from " + table + " where `YEAR`=?"
    data = curs.execute(stmt, (YEAR, ))
    # for d in data:
    #     print(d)
    item = curs.fetchone()
    df["date"] = [description[0] for description in curs.description]
    df = df[12:]  # HACK should be 4
    df['date'] = df['date'].str.replace('/', '')
    df['date'] = pd.to_datetime(df['date'], format='%m%d%y')
    df["Open"] = item[12:]  # HACK should be 4
    conn.close()
    return df


def db_get_locales():
    conn = sl.connect(db)
    curs = conn.cursor()

    table = "tesla"
    stmt = "SELECT `YEAR` from " + table
    data = curs.execute(stmt)
    # sort a set comprehension for unique values
    locales = sorted({result[0] for result in data})
    conn.close()
    return locales




# m = "SELECT * FROM time_series_confirmed WHERE `Country/Region`='France'"
# result = conn.execute(m)

@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for("home"))

if __name__ == "__main__":
    #print(db_get_locales())
    #db_create_dataframe("Amazon", "2010")
    app.secret_key = os.urandom(12)
    app.run(debug=True)
