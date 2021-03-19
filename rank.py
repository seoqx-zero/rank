# 根据阿布云的动态版情况来设置
THREADS = 5 # 每秒请求数是多少就设置多少线程数量
USER = 'H6572MC9352ZXW3D' # 通行证书
PASS = '0006AC9E5B6B9B07' # 通行密钥

proxies = {
    'https': f'http://{USER}:{PASS}@http-dyn.abuyun.com:9020',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
}

def rank_tn(query):
    if '--760' in sys.argv[1]:
        pn_max = 760
    else:
        pn_max = 50

    results = []
    for pn in range(0, pn_max, 50):
        while 1:
            try:
                if '--no-proxy' not in sys.argv:
                    data = requests.get('https://www.baidu.com/s', {'wd': query, 'rn': 50, 'tn': 'json', 'pn': pn}, headers=headers, proxies=proxies).json()
                else:
                    data = requests.get('https://www.baidu.com/s', {'wd': query, 'rn': 50, 'tn': 'json', 'pn': pn}, headers=headers).json()
            except:
                print('NET ERR')
                time.sleep(0.2)
            else:
                break

        for item in data['feed']['entry'][:-1]:
            results.append((
                item.get('url', '-'),
                item.get('title', '-'),
            ))
    return query, results
  
threads_count = THREADS if '--no-proxy' not in sys.argv else 1
with futures.ThreadPoolExecutor(max_workers=threads_count) as executor:
    queries = [ line.rstrip() for line in open(input_file) if line.rstrip() not in already ]
    pbar = tqdm(total=len(queries))

    if '--mobile' in sys.argv:
        to_do = [ executor.submit(rank_mobile, query) for query in queries ]
    elif '--normal' in sys.argv:
        to_do = [ executor.submit(rank_normal, query) for query in queries ]
    else:
        to_do = [ executor.submit(rank_tn, query) for query in queries ]

    for future in futures.as_completed(to_do):
        query, results = future.result()
        f.write(json.dumps({
            'query': query,
            'results': results
        })+'\n')
        pbar.update(1)
