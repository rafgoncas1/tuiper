import time
import argparse
import aiohttp
import asyncio
import tqdm.asyncio

async def send_request(session, url):
    async with session.post(url):
        pass

async def blast(url, numrequests):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url) for _ in range(numrequests)]
        for task in tqdm.asyncio.tqdm.as_completed(tasks):
            await task

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blast a tuiper with requests.')
    parser.add_argument('-id', '--id', help='Tuip ID', required=True, type=int)
    parser.add_argument('-n', '--n', help='Number of requests', required=True, type=int)
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
            parser.print_help()

    start_time = time.time()
    
    print(f"\n\n##### Blast started #####\n\n* requests: {args.n}\n* tuip ID: {args.id}\n")
    
    asyncio.run(blast(f'http://localhost:8000/api/like/{args.id}/blast', args.n))

    end_time = time.time()

    print(f'\n{args.n} requests sent in {end_time-start_time} seconds')