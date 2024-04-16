import requests
import concurrent.futures
import time
import argparse

# Función para enviar una petición al servidor
def send_request(url):
    requests.post(url)

def blast(url, numrequests):
   with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(send_request, [url] * numrequests)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blast a tuiper with requests.')
    parser.add_argument('-id', '--id', help='Tuip ID', required=True, type=int)
    parser.add_argument('-n', '--n', help='Number of requests', required=True, type=int)
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
            parser.print_help()

    start_time = time.time()
    
    blast(f'http://localhost:8000/api/like/{args.id}/blast', args.n)

    end_time = time.time()

    print(f'Tiempo transcurrido: {end_time - start_time} segundos. Peticiones totales enviadas: {args.n}')