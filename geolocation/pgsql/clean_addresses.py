

def clean_street_names(df,from_label,to_label):
    def remove_non_ascii(text):
        return re_sub(r'[^\x00-\x7F]+',' ', text)

    df_ignore = df[df[from_label].map(lambda s: type(s))==NoneType]
    df = df.ix[df.index-df_ignore.index,:]

    df[to_label]=df[from_label].map(lambda s: s.lower().strip())
    df[to_label]=df[to_label].map(remove_non_ascii)

    # st_strip_before
    for k,v in ST_STRIP_BEFORE_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(k,v,s))

    # st_prefix
    for k,v in ST_PREFIX_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(r'^('+k+r')\s',v+r' ',s)
                                        if ST_SUFFIX_DICT.values().count(
                                        re_sub(r'^('+k+r')\s',v+r' ',s)
                                        ) == 0 else s)

    # st_suffix
    for k,v in ST_SUFFIX_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(r'\s('+k+r')$'   ,r' '+v,s))

    # st_body
    for k,v in ST_BODY_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(k,v,s))

    # st_strip_after
    for k,v in ST_STRIP_AFTER_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(k,v,s))

    return df.append(df_ignore)