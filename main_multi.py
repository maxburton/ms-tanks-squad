import concurrent.futures
import main


def main_multi():
    executor: concurrent.futures.Executor
    executor = concurrent.futures.ProcessPoolExecutor()
    for i in range(0, 4):
        executor.submit(main.main, False, '127.0.0.1', 8052, f'Human:{i}')
    executor.shutdown()


if __name__ == '__main__':
    main_multi()
