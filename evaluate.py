import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def ifXcontainsY(x_list, y_list):
    ct = 0 
    flag = False
    if 'ADJ' in y_list and 'V.PTCP' in y_list:
        flag = True
    for y in y_list:
        if flag is True:
            if y == 'V.PTCP':
                ct = ct+1
                continue
        if y in x_list:
            ct = ct+1
    if ct == len(y_list):
        return True
    else:
        return False
    
def compatibleWithXandY(feas,fea_list):
    done = False
    if 'ADJ' in feas:
        for fea in fea_list:
            if fea.startswith('ADJ;') or (';ADJ' in fea) or fea=='ADJ':
                done = True
                break
    elif 'N' in feas:
        for fea in fea_list:
            if fea.startswith('N;') or (';N;' in fea) or fea.endswith(';N'):
                done = True
                break
    else:
        return True
    return done

def plusFeatures(prefix, plus_sets):
    ans = []
    if len(plus_sets) == 0:
        ans.append(prefix)
        return ans
    plus_set = plus_sets[0]
    leftover = plus_sets[1:]
    for feature in plus_set:
        ans.extend(plusFeatures(prefix+';'+feature, leftover))
    return ans

def constructFeatureSets(features):
    single_features = []
    plus_sets = []
    feas = features.split(';')
    ans = []
    for feature in feas:
        if ('+' in feature) is False:
            single_features.append(feature)
        else:
            plus_sets.append(feature.split('+'))

    feature_form = ';'.join(sorted(single_features))
    
    if len(plus_sets) > 0:
        all_variations = plusFeatures('',plus_sets)
        for variaty in all_variations:
            variaty = feature_form + variaty
            ans.append(';'.join(sorted(variaty.split(';'))))
    else:
        ans.append(feature_form)
    return ans


def readDataSet(filepath, pos):
    with open(filepath, 'r', encoding = 'utf-8') as f:
        ds_lines = f.read().split('\n')
    dataset = {}
    for i in range(len(ds_lines)):
        parts = ds_lines[i].split('\t')
        if len(parts) < 3:
            continue
        if pos in set(parts[2].split(';')): 
            continue
        wp_str = parts[0].lower()+'_sep_'+parts[1].lower()
        if wp_str in dataset:
            current_set = dataset[wp_str]
        else:
            current_set = set()
        current_set.update(constructFeatureSets(parts[2]))
        dataset[wp_str] = current_set
    f.close()
    return dataset

def findCorePOS(um_set):
    core_POS= ['V','N','ADJ','ADV','V.PTCP','V.CVB','V.MSDR']
    for pos in core_POS:
        if pos in um_set:
            return pos
    return 'n.a'

def print_numbers(stats_dict, log):
    if len(log) > 1:
        print('----- incorrectness details -----')
        for key in log:
            print(key.split('_')[0],key.split('_')[1],log[key])
        print('---------------------------------')
    for stat_name, stat in sorted(stats_dict.items()):
        print("\t".join([stat_name, "{:.2f}".format(stat)]))


def evaluate(ud_dataset, um_dataset, log):
    total, cov_ct, pr_ct  = 1.0, 1.0, .0
    incorrect = {}
    for key in ud_dataset:
        total = total + len(ud_dataset[key])
        if (key in um_dataset) is False:
            continue
        lemma, form = key.split('_sep_')
        found = False
        predict = False
        for ud_features in ud_dataset[key]:
            ud_set = set(ud_features.split(';'))
            ud_pos = findCorePOS(ud_set)
            for um_features in um_dataset[key]:
                um_set = set(um_features.split(';'))
                if (ud_pos in um_set) is False:
                    continue
                found = True
                if ifXcontainsY(um_features.split(';'), ud_features.split(';')):
                    predict = True
                elif log:
                    log_instance = ud_features +'_'+um_features
                    if log_instance in incorrect:
                        incorrect[log_instance] = incorrect[log_instance] + 1
                    else:
                        incorrect[log_instance] = 1
        if found == True:
            cov_ct = cov_ct + 1
            if predict == True:
                pr_ct = pr_ct + 1

    precision = 100 * pr_ct / cov_ct
    recall = 100 * pr_ct / total
    if precision+recall == 0:
        f_measure = .0
    else:
        f_measure = 2 * precision * recall / (precision + recall)
    return {"precision": precision, "recall": recall, "f-measure": f_measure}, incorrect

def main(args):
    um_dataset = readDataSet(args.unimorph, args.pos)
    ud_dataset = readDataSet(args.gold, args.pos)
    overall_stats, log = evaluate(ud_dataset, um_dataset, args.log)
    print_numbers(overall_stats, log)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Unimorph evaluation on Treebanks of Universal Dependencies')
    parser.add_argument("--gold", help="Gold Treebank", required=True, type=str)
    parser.add_argument("--unimorph", help="Unimorph file", required=True, type=str)
    parser.add_argument("--pos", help="V or N or ADJ", required=False, type=str)
    parser.add_argument("--log", help="True of False", required=False, type=bool)
    opt = parser.parse_args()
    main(opt)