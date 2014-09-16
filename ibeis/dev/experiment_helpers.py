from __future__ import absolute_import, division, print_function
import utool
import six
from six.moves import zip, map
import re
from ibeis.dev import experiment_configs
from ibeis.model import Config
print, print_, printDBG, rrr, profile = utool.inject(
    __name__, '[expt_helpers]', DEBUG=False)

QUIET = utool.QUIET


def get_vary_dicts(test_cfg_name_list):
    vary_dicts = []
    for cfg_name in test_cfg_name_list:
        test_cfg = experiment_configs.__dict__[cfg_name]
        vary_dicts.append(test_cfg)
    if len(vary_dicts) == 0:
        valid_cfg_names = experiment_configs.TEST_NAMES
        raise Exception('Choose a valid testcfg:\n' + valid_cfg_names)
    for dict_ in vary_dicts:
        for key, val in six.iteritems(dict_):
            assert not isinstance(val, str), 'val should be list not string: not %r' % (type(val),)
            #assert not isinstance(val, (list, tuple)), 'val should be list or tuple: not %r' % (type(val),)
    return vary_dicts


def rankscore_str(thresh, nLess, total):
    #helper to print rank scores of configs
    percent = 100 * nLess / total
    fmtsf = '%' + str(utool.num2_sigfig(total)) + 'd'
    fmtstr = '#ranks < %d = ' + fmtsf + '/%d = (%.1f%%) (err=' + fmtsf + ')'
    rankscore_str = fmtstr % (thresh, nLess, total, percent, (total - nLess))
    return rankscore_str


def wrap_cfgstr(cfgstr):
    # REGEX to locate _XXXX(
    cfg_regex = r'_[A-Z][A-Z]*\('
    cfgstrmarker_list = re.findall(cfg_regex, cfgstr)
    cfgstrconfig_list = re.split(cfg_regex, cfgstr)
    args = [cfgstrconfig_list, cfgstrmarker_list]
    interleave_iter = utool.interleave(args)
    new_cfgstr_list = []
    total_len = 0
    prefix_str = ''
    # If unbalanced there is a prefix before a marker
    if len(cfgstrmarker_list) < len(cfgstrconfig_list):
        frag = interleave_iter.next()
        new_cfgstr_list += [frag]
        total_len = len(frag)
        prefix_str = ' ' * len(frag)
    # Iterate through markers and config strings
    while True:
        try:
            marker_str = interleave_iter.next()
            config_str = interleave_iter.next()
            frag = marker_str + config_str
        except StopIteration:
            break
        total_len += len(frag)
        new_cfgstr_list += [frag]
        # Go to newline if past 80 chars
        if total_len > 80:
            total_len = 0
            new_cfgstr_list += ['\n' + prefix_str]
    wrapped_cfgstr = ''.join(new_cfgstr_list)
    return wrapped_cfgstr


def format_cfgstr_list(cfgstr_list):
    indented_list = utool.indent_list('    ', cfgstr_list)
    wrapped_list = list(map(wrap_cfgstr, indented_list))
    return utool.joins('\n', wrapped_list)


#---------------
# Big Test Cache
#-----------

def get_varied_params_list(test_cfg_name_list):
    vary_dicts = get_vary_dicts(test_cfg_name_list)
    dict_comb_list = [utool.all_dict_combinations(dict_) for dict_ in vary_dicts]
    dict_comb_lbls = [utool.all_dict_combinations_lbls(dict_) for dict_ in vary_dicts]
    # Append testname
    dict_comb_lbls = [[name_lbl + lbl for lbl in comb_lbls] for name_lbl, comb_lbls in zip(test_cfg_name_list, dict_comb_lbls)]
    varied_params_list = utool.flatten(dict_comb_list)  # [comb for dict_comb in dict_comb_list for comb in dict_comb]
    varied_param_lbls = utool.flatten(dict_comb_lbls)
    return varied_params_list, varied_param_lbls


def _get_cfg_list(test_cfg_name_list):
    varied_params_list, varied_param_lbls = get_varied_params_list(test_cfg_name_list)
    # Add unique configs to the list
    cfg_list = []
    cfgx2_lbl = []
    cfg_set = set([])
    for dict_, lbl in zip(varied_params_list, varied_param_lbls):
        cfg = Config.QueryConfig(**dict_)
        if cfg not in cfg_set:
            cfgx2_lbl.append(lbl)
            cfg_list.append(cfg)
            cfg_set.add(cfg)
    if not QUIET:
        print('[harn] return %d / %d unique configs' % (len(cfg_list), len(varied_params_list)))
    return cfg_list, cfgx2_lbl


def get_cfg_list(test_cfg_name_list, ibs=None):
    print('[harn] building cfg_list: %s' % test_cfg_name_list)
    if 'custom' == test_cfg_name_list:
        # Usee the ibeis config as a custom config
        print('   * custom cfg_list')
        cfg_list = [ibs.cfg.query_cfg]
        cfgx2_lbl = ['custom']
        return cfg_list, cfgx2_lbl
    return _get_cfg_list(test_cfg_name_list)


def get_cfg_list_and_lbls(test_cfg_name_list, ibs=None):
    """
    Returns a list of varied query configurations. Only custom configs depend on
    IBEIS
    """
    cfg_list, cfgx2_lbl = get_cfg_list(test_cfg_name_list, ibs=ibs)
    print(cfgx2_lbl)
    # cfgx2_lbl denotes which parameters are being varied.
    # If there is just one config then nothing is varied
    return cfg_list, cfgx2_lbl
