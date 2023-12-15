import psycopg2
import matplotlib.pyplot as plt

username = 'postgres'
password = '12345'
database = 'LAB3'
host = 'localhost'
port = '5432'

query_1 = '''
    SELECT imdb_rating, film_name FROM film
    JOIN genre ON film.film_id = genre.film_id
    WHERE genre = 'Drama' 
    or genre = 'Action'
'''

query_2 = '''
    SELECT film_name, runtime FROM film
    JOIN director ON film.director_id = director.director_id
    WHERE director.film_count > 10;
'''

query_3 = '''
    SELECT name FROM director
    JOIN film ON director.director_id = film.director_id
    JOIN genre ON film.film_id = genre.film_id
    WHERE genre = 'History'
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()

    cur.execute(query_1)
    anim_genre = []
    total = []

    for row in cur:
        anim_genre.append(row[1])
        total.append(row[0])

    x_range = range(len(anim_genre))

    figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)
    bar = bar_ax.bar(x_range, total, label='Total')
    bar_ax.bar_label(bar, label_type='center', fmt='%d')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(anim_genre, rotation=90)
    bar_ax.set_xlabel('Назви фільмів')
    bar_ax.set_yticks(bar_ax.get_yticks())
    bar_ax.set_yticklabels(str(int(float(label))) for label in bar_ax.get_yticks())
    bar_ax.set_ylabel('рейтинг')
    bar_ax.set_title('Рейтинг фільмів')


    cur.execute(query_2)
    film_name = []
    runtime = []

    for row in cur:
        film_name.append(row[0])
        runtime.append(row[1])

    pie_ax.pie(runtime, labels=film_name, autopct='%1.01f%%')
    pie_ax.set_title('Частка фільму за продовжиністтю')

    cur.execute(query_1)
    count = []
    rating = []

    for row in cur:
        count.append(row[1])
        rating.append(row[0])

    graph_ax.plot(count, rating, color='blue', marker='o')

    for cnt, rat in zip(count, rating):
        graph_ax.annotate(rat, xy=(cnt, rat), color='blue',
                           textcoords='offset points')

    graph_ax.set_xlabel('фільм')
    graph_ax.set_ylabel('Рейтинг')
    graph_ax.set_title('Графік залежності рейтингу фільму від фільму')


mng = plt.get_current_fig_manager()
mng.resize(1700, 900)

plt.show()