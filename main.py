import psycopg2

DB_PARAMS = {
    'host': 'localhost',
    'database': 'LAB3',
    'user': 'postgres',
    'password': '12345',
    'port': '5432'
}

QUERIES = {
    'query_1': '''
        SELECT imdb_rating, film_name FROM film
        JOIN genre ON film.film_id = genre.film_id
        WHERE genre = 'History' 
        or genre = 'Action';
    ''',
    'query_2': '''
        SELECT film_name FROM film
        JOIN director ON film.director_id = director.director_id
        WHERE director.film_count > 30;
    ''',
    'query_3': '''
        SELECT name FROM director
        JOIN film ON director.director_id = film.director_id
        JOIN genre ON film.film_id = genre.film_id
        WHERE genre = 'History';
    '''
}

def execute_query(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def print_query_results(query, result):
    print(f"\nResults for Query: {query}\n")
    for row in result:
        print(" - ".join(map(str, row)))
    print()

def main():
    with psycopg2.connect(
        user=DB_PARAMS['user'],
        password=DB_PARAMS['password'],
        dbname=DB_PARAMS['database'],
        host=DB_PARAMS['host'],
        port=DB_PARAMS['port']
    ) as connection:
        with connection.cursor() as cursor:
            for query_name, query in QUERIES.items():
                result = execute_query(cursor, query)
                print_query_results(query_name, result)

if __name__ == '__main__':
    main()