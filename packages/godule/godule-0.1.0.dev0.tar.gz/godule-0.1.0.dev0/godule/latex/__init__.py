def _find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def _get_bold_idxs(latex_rows, column_idxs, row_idxs):
    maxes = {col: None for col in column_idxs.keys()}
    for idx in row_idxs:
        for column, (start, end) in column_idxs.items():
            val = latex_rows[idx][start:end].strip(r'\ ')
            try:
                val = float(val)
                if maxes[column] is None:
                    maxes[column] = val
                maxes[column] = max(maxes[column], val)
            except:
                pass
    bold = {row: {col: False for col in column_idxs} for row in row_idxs}
    for idx in row_idxs:
        for column, (start, end) in column_idxs.items():
            val = latex_rows[idx][start:end].strip(r'\ ')
            try:
                val = float(val)
                bold[idx][column] = (val >= maxes[column])
            except:
                pass
    return bold

def _get_bolded_table(latex_str, columns):
    from more_itertools import windowed
    latex_rows = latex_str.split('\n')
    column_row = latex_rows[latex_rows.index('\\toprule') + 1]
    amp_idxs = [0, *_find(column_row, '&'), len(column_row.rsplit('\\\\')[0])]
    column_idxs = dict()
    for idx, (column, (start, end)) in enumerate(zip(columns, windowed(amp_idxs, 2))):
        column_idxs[column] = (start + int(idx != 0), end)
    row_idxs = list(range(latex_rows.index('\\midrule') + 1, latex_rows.index('\\bottomrule')))
    bold_idxs = _get_bold_idxs(latex_rows, column_idxs, row_idxs)
    columns_order = list(map(lambda x: x[0], sorted(column_idxs.items(), key=lambda x: -x[1][1])))
    for column in columns_order:
        for idx in row_idxs:
            if bold_idxs[idx][column]:
                start, end = column_idxs[column]
                length = end - start
                latex_rows[idx] = latex_rows[idx][:start] + r'{\bf ' + \
                    latex_rows[idx][start:start + length] + '}' + latex_rows[idx][start + length:]
    return '\n'.join(latex_rows)

def to_table(pd_table, float_format, label, bold_max_columns=True):
    latex_table = pd_table.to_latex(
        index=False,
        na_rep='-',
        float_format=float_format,
        index_names=True,
        bold_rows=True,
        escape=False,
        label=label,
        position='H'
    )
    if bold_max_columns:
        latex_table = _get_bolded_table(latex_table, pd_table.columns)
    return latex_table
