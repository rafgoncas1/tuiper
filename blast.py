import time
import argparse
import aiohttp
import asyncio

async def send_request(session, url):
    async with session.post(url):
        pass

async def blast(url, numrequests):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url) for _ in range(numrequests)]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blast a tuiper with requests.')
    parser.add_argument('-id', '--id', help='Tuip ID', required=True, type=int)
    parser.add_argument('-n', '--n', help='Number of requests', required=True, type=int)
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
            parser.print_help()

    start_time = time.time()
    
    asyncio.run(blast(f'http://localhost:8000/api/like/{args.id}/blast', args.n))

    end_time = time.time()

    print(f'Tiempo transcurrido: {end_time - start_time} segundos. Peticiones totales enviadas: {args.n}')