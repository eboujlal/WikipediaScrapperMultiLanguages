import time,urllib,os

def create_dir(path):
    if not folder_exist(path):
        os.makedirs(path)
        return True
    return False

def fetch_start_urls():
    with open('start_urls.txt', 'r') as f:
        urls = f.readlines()
        return [u.strip('\n') for u in urls]


def folder_exist(path):
    return os.path.exists(path)

def count_files(path):
    return len([name for name in os.listdir(path) if os.path.isfile(name)])

def printProgressBar (iteration, total, prefix= '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                        (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()
