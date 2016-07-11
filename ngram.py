# coding=utf-8
import os
import sys
import operator

PUNCTUATION_LIST = u'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。';

def split_file(file_path, output_dir, piece_gega_bytes=5):
    piece_bytes = piece_gega_bytes * 1000000000
    print '[START] split file...'
    if not output_dir.endswith('/'):
        output_dir += '/'

    if not output_dir.startswith('/tmp/'):
        print 'ERROR: output_dir must in /tmp/ directory'
        return

    if os.path.exists(output_dir):
        os.system('rm -rf ' + output_dir)
        os.system('rm -rf ' + output_dir[:-1] + '_ngram/')

    os.system('mkdir ' + output_dir)
    os.system('mkdir ' + output_dir[:-1] + '_ngram/')

    os.system('split -b ' + str(int(piece_bytes)) + ' ' + file_path + ' ' + output_dir)
    print '[END] split file...'

def not_filter(tu):
    return True

def default_filter(tu):
    filter_characters = set(u'的是个就有一也这在把是呢吗了要着还' + PUNCTUATION_LIST)
    filter_word = set([u'那么',u'我们', u'可以', u'所以', u'这样', u'这个', u'另外', u'一个'])
    filter_characters |= filter_word
    segs = [c.decode('utf-8') for c in tu[0].split(' ')]
    if any((c in filter_characters) for c in segs):
        return False
    return True

def punctuation_filter(tu):
    filter_characters = set(PUNCTUATION_LIST)
    filter_word = set([])
    filter_characters |= filter_word
    segs = [c.decode('utf-8') for c in tu[0].split(' ')]
    if any((c in filter_characters) for c in segs):
        return False
    return True

def get_ngram(gram_num, file_path, output_path, filter_num=0):
    ngram_dict = {}
    ngram_file = open(output_path, 'w')
    with open(file_path, 'r') as text_file:
        counter = 0
        for line in text_file:
            line = line.strip()
            segs = line.split(' ')

            for index in range(0, len(segs) - gram_num + 1):
                ngram = ' '.join(segs[index:index + gram_num])
                #print ngram
                if ngram not in ngram_dict:
                    ngram_dict[ngram] = 0
                ngram_dict[ngram] += 1

            if counter % 100000 == 0:
                print counter
            counter += 1

    counter = 0
    for key,value in ngram_dict.iteritems():
        if value <= filter_num:
            continue
        ngram_file.write(key + '\t' + str(value) + '\n')

        if counter % 10000 == 0:
            print counter
        counter += 1

    ngram_file.close()

def merge_ngram_file(ngram_file_list, output_path, sort=False, filter_function=not_filter, merge=False):
    '''
    Sample format of ngram_file_list: [(name, path), (name, path), ...]
    '''
    ngram_dict = {}
    for ngram_file_path in ngram_file_list:
        with open(ngram_file_path, 'r') as ngram_file:
            for line in ngram_file:
                line = line.strip()
                segs = line.split('\t')
                if segs[0] not in ngram_dict:
                    ngram_dict[segs[0]] = 0
                try:
                    ngram_dict[segs[0]] += int(segs[1])
                except:
                    print line

    with open(output_path, 'w') as output_file:
        if not sort:
            for key, value in ngram_dict.iteritems():
                if not filter_function((key, value)):
                    continue
                if merge:
                    key = key.replace(' ', '')
                output_file.write(key + '\t' + str(value) + '\n')
        else:
            ngram_sorted = sorted(ngram_dict.items(), key=operator.itemgetter(1), reverse=True)
            for tu in ngram_sorted:
                if not filter_function(tu):
                    continue
                key = tu[0]
                value = tu[1]
                if merge:
                    key = key.replace(' ', '')
                output_file.write(key + '\t' + str(value) + '\n')

def generate_large_ngram_by_filtering(file_path, output_path,  gram_num=3, filter_num=3, sort=False, filter_function=not_filter,merge=False):
    tmp_dir = '/tmp/large_ngram_pieces/'
    piece_ngram_dir = '/tmp/large_ngram_pieces_ngram/'

    # split file to 5g pieces

    split_file(file_path, tmp_dir, 5)

    # generate pieces ngram files
    piece_file_list = [(f, os.path.join(tmp_dir, f)) for f in os.listdir(tmp_dir)]
    piece_ngram_list = []

    for piece_file_tuple in piece_file_list:
        piece_file_name = piece_file_tuple[0]
        piece_file_path = piece_file_tuple[1]
        piece_ngram_path = piece_ngram_dir + piece_file_name + '_n' + str(gram_num)
        piece_ngram_list.append(piece_ngram_path)
        get_ngram(gram_num, piece_file_path, piece_ngram_path, filter_num=filter_num)

    merge_ngram_file(piece_ngram_list, output_path, sort, filter_function, merge)

def remove_frequency(file_path, output_path, fre_threshold=None):
    if output_path == None:
        output_path = file_path + '_fre_removed'
    with open(file_path) as input_file:
        with open(output_path,'w') as output_file:
            for line in input_file:
                line = line.strip()
                line_fre = int(line.split('\t')[1])
                if fre_threshold:
                    if line_fre < fre_threshold:
                        continue
                output_file.write(line.split('\t')[0] + '\n')

def ngram_count(input_file_path, output_file_path, gram_num, filter_num, merge=False, sort=True):
    generate_large_ngram_by_filtering(input_file_path, output_file_path, gram_num=gram_num, filter_num=filter_num, filter_function=punctuation_filter, merge=merge)

def load_ngram(ngram_file_path):
    ngram_dict = {}
    with open(ngram_file_path) as ngram_file:
        for line in ngram_file:
            line = line.strip()
            ngram, gram_count = line.split('\t')
            ngram_dict[ngram] = int(gram_count)
    return ngram_dict

if __name__ == '__main__':
    func = sys.argv[1]

    if func == 'ngram_count':
        input_file_path, output_file_path, gram_num, filter_num = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
        generate_large_ngram_by_filtering(input_file_path, output_file_path, gram_num=gram_num, filter_num=filter_num, sort=True, filter_function=punctuation_filter, merge=False)
    elif func == 'segment':
        input_file_path, output_file_path = sys.argv[2], sys.argv[3]
        seg_file(input_file_path, output_file_path)
