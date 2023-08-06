import argparse
import asyncio

from loyalcat.http import HttpClient, Route


p = argparse.ArgumentParser()
p.add_argument('-a', '--action', help='動作', default='ci')
p.add_argument('-c', '--commit_hash', help='VCSのコミットハッシュ', default=None)
p.add_argument('-p', '--project_id', help='対象のプロジェクトID', default=None)
p.add_argument('-s', '--status', help='結果', default=None)
args = p.parse_args()


async def create_pipeline(api: HttpClient):
    if args.commit_hash is None or args.project_id is None:
        raise Exception('-c, -pのどちらかが不足しています')
    res = await api.request(Route('POST', '/api/pipelines/:id', params={':id': args.project_id}), body={'commitHash': args.commit_hash})
    print(res.get('url'))
    while True:
        status_check = await api.request(Route('GET', '/api/pipelines/:id', params={':id': res.get('id')}))
        if status_check.get('isDone', False) is True:
            await api.session.close()
            print(status_check)
            if status_check.get('type', 'success') == 'success':
                print('success')
                exit(0)
            else:
                raise Exception('CI failure')
        await asyncio.sleep(3)

async def finished_pipeline(api: HttpClient):
    if args.commit_hash is None or args.status is None:
        raise Exception('-c, -sが不足しています')
    await api.request(Route('POST', '/api/pipelines/:id/update', {':id': args.commit_hash}), body={'status': args.status})

async def _main():
    api = HttpClient().create_session()

    match args.action:
        case 'ci': await create_pipeline(api)
        case 'finish': await finished_pipeline(api)
    await api.session.close()
def main() -> None:
    asyncio.run(_main())
        
    