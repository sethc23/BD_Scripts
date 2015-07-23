#!/home/ub2/.scripts/ENV/bin/python

from ipdb import set_trace as i_trace

class Trulia:

	def __init__(self):
		from os                             import environ          as os_environ
		from sys                            import path             as py_path
		py_path.append(                         os_environ['HOME'] + '/BD_Scripts/html')
		from preview_autopost 				import Auto_Poster
		x 									= 	Auto_Poster()
		self.T 								= 	x.T

	
	def scrape_feed_data(self):
		def convert_dev_guide_to_xml(xml_f):
			# http://static.trulia-cdn.com/resources/TruliaDevGuide.pdf
			dev_guide 						= 	'TruliaDevGuide.pdf'
			assert self.T.os_path_exists(dev_guide)
			cmd 							= 	'pdftohtml -f 4 -l 11 -i -stdout -xml %s > ./%s' % (dev_guide,xml_f)
			(_out,_err) 					= 	self.T.exec_cmds([cmd])
			assert not _out
			assert _err is None
			return

		xml_f 								= 	'trulia.xml'
		if not self.T.os_path_exists(xml_f):
			convert_dev_guide_to_xml(xml_f)
		assert self.T.os_path_exists(xml_f)
		 
		
		with open(xml_f,'r') as f: 		x 	=	f.readlines()

		h 									=	self.T.getSoup(''.join(x))
		df 									= 	self.T.pd.DataFrame(columns=['row'],data=h.find_all('text'))
		df['text'] 							= 	df.row.map(lambda r: r.text)
		cols 								=	df.row.tolist()[0].attrs.keys()
		for it in cols:
			df[it] 							= 	df.row.map(lambda r: int(r.get(it)))


		header_start 						= 	'Element Name'
		header_end 							= 	'Enumerations/Sample Value'

		s,e 								=	'',''
		for idx,it in df.iterrows():
			if str(it.text).strip()==header_start:
				s 							=	idx
			if s and str(it.text).strip()==header_end:
				e 							=	idx
				break

		take_header 						= 	df.ix[s:e,'text'].tolist()
		header_row 							=	[it.strip().replace(' ','_').lower() for it in df.ix[s:e,'text'].tolist()]
		col_pts 							= 	df.ix[s:e,'left'].astype(int).tolist()
		header_cols 						= 	dict(zip(header_row,col_pts))

		# Remove pre-header row content
		df 									= 	df.ix[e+1:,:].reset_index(drop=True)

		# Remove subsequent header rows, i.e., top row on each page
		header_col_len,pop_list 			= 	len(header_row),[]
		for k,v in df.iterrows():
			if k+header_col_len>len(df):
				break
			if df.ix[k:k+header_col_len-1,'text'].tolist() == take_header:
				pop_list.append(				k)
		df 									= 	df.drop(pop_list,axis=0).reset_index(drop=True)

		# Identify First Values of Each Row
		tag_names 							= 	[it for it in df[df.left<col_pts[1]].text.tolist() if self.T.re_findall(r'^<',it[0])]
		df['element_start'] 				= 	df.text.map(lambda r: True if tag_names.count(r) else False)

		# BUG FIX (align to sub_depth 1)
		df['left'] 							= 	df.left.map(lambda n: n if not [86,92].count(n) else 87)
		# BUG FIX (align to sub_depth 2)
		df['left'] 							= 	df.left.map(lambda n: n if not [95].count(n) else 109)

		# Create Indicators for Depth of Sub-Elements
		uniq_first_col_pts 					=	sorted(df[df.element_start==True].left.astype(int).unique().tolist())
		df['depth'] 						=	df.left.map(lambda r: None if not uniq_first_col_pts.count(int(r))
		                                			else uniq_first_col_pts.index(int(r)))

		# Make DataFrame from Specs
		t 									= 	self.T.pd.DataFrame(columns=header_row)
		sub_element_depths					= 	[]
		for idx,r in df.iterrows():
			if r.element_start==True:

				# # if next element is a new row: pass
				# if not r.top==df.ix[idx+1,'top']:
				# if df.ix[idx+1,'element_start']==True:
				# 	d 						=   { header_row[0] 			:	r.}
				# 	d.update(dict(zip( 			header_row[1:], [None for i in range(len(header_row[1:]))])))
				# # else: process rows until next new row
				# else:

				d 							= 	{	'depth'					:	r.depth}
				pt,header_pt 				= 	0,0
				while True:
					r 						= 	df.ix[pt+idx,:]
					
					# if r.text=='<city-name/>':
					# 	i_trace()

					# if next text starts in the same col
					if r.name>0 and (	r.left==df.ix[pt+idx-1,'left']
										or header_pt==len(col_pts)
										or r.left<col_pts[header_pt]):
						header_pt 	   	   -= 	1
						header_pt			=	0 if header_pt<0 else header_pt



					if d.has_key(header_row[header_pt]):
						d.update({ 				header_row[header_pt]		: 	d[header_row[header_pt]].rstrip('-') + r.text.lstrip('-')})
					else:
						d.update({ 				header_row[header_pt]		:	r.text 	})


					if len(df)==pt+idx+1 or df.ix[pt+idx+1,'element_start']==True:
						# if len(d.keys())-1!=len(header_row):
						# 	i_trace()
						break
					else:
						pt 			   	   +=	1
						header_pt 	       +=	1

				t 							= 	t.append(d,ignore_index=True)
		
		# Clean Up:
		
		# 1. any row with element_name and header_row values -> header_row
		for i in range(len(take_header)):
			t[header_row[i]] 				=	t[header_row[i]].map(lambda c: None if c==take_header[i] else c)
		
		# 2. harmonize null value types
		for it in header_row:
			t[it] 							= 	t[it].map(lambda r: '' if self.T.pd.isnull(r) or r==None else r)

		# 3. ID container tags
		t['container'] 						= 	False
		for k,v in t.iterrows():
			tmp 							= 	v[1:5].unique().tolist()
			if not tmp or (len(tmp)==1 and tmp[0]==''):
				t.ix[k,'container'] 		=	True
			if t.ix[k:k,3].str.contains(' container ',case=False).all():
				t.ix[k,'container'] 		=	True

		# 4. ID repeatable container elements
		t['repeatable'] 					=	False
		repeat_idx 							=	t[t.required.str.contains('Repeatable',case=False)].index.tolist()
		t.ix[repeat_idx,'repeatable'] 		=	True
		t.ix[repeat_idx,header_row[3]] 		=	t.ix[repeat_idx,header_row[1]].map(lambda r: '| '+r)
		t.ix[repeat_idx,header_row[1]] 		=	''

		# 5. Clean up element name column
		t[header_row[0]] 					= 	t[header_row[0]].map(lambda c: c[:c.rfind('>')+1])

		####
		## -- BUG/INCONSISTENCY FIXES
		####
		# 1. additional containers
		idx 								=	t[t.required.str.contains('Container',case=False)].index.tolist()
		t.ix[idx,[header_row[1],'container']]=	['',True]
		# 2.
		idx 								= 	t[t.element_name=='<hoa-fees>'].index
		t 									=	t.drop(idx,axis=0).reset_index(drop=True)
		# 3.
		idx 								= 	t[t.element_name=='<office/>'].index
		t.ix[idx,[1,3]] 					=	['','| ' + t.ix[idx,1]]
		# 4.
		idx 								= 	t[t.element_name=='<rental-terms/>'].index
		t.ix[idx,[1,3]] 					=	['','| ' + t.ix[idx,1]]
		# 5. fix tag that was at end of page and combined with header row
		idx 								= 	t[t.element_name=='<has-pond/>'].index
		idx_val 							=	t.ix[idx,4].tolist()[0]
		t.ix[idx,4] 						=	idx_val[:idx_val.find(')')+1]
		# 6. fix formats with 'No'
		idx 								= 	t[ t[header_row[3]].isin(['Yes','No','yes','no']) ].index
		t.ix[idx,[3,4]]						=	['Boolean','(yes | no)']
		# 7. adjust 'repeatable' col based on 'description' col
		idx 								= 	t[ (t[header_row[3]].str.contains('repeatable',case=False)) & (t.repeatable==False) ].index
		t.ix[idx,'repeatable'] 				=	True

		# Split Format & Description Columns
		for it in header_row[3:4]:
			t[it] 							= 	t[it].map(lambda c: c.strip())
		formats 							= 	['String','Integer','Decimal','Boolean','Year','Enumerated','URL','Recommended']
		formats_lower 						= 	[it.lower() for it in formats]

		t['format_type'] 					= 	''
		# -- single word formats
		idx 								= 	t[ t[header_row[3]].isin(formats) ].index
		t.ix[idx,'format_type'] 			= 	t.ix[idx,header_row[3]]
		# -- single word before '|'
		idx 								= 	t[ t[header_row[3]].str.replace(r'[\s]*\|.*','').isin(formats) ].index
		t.ix[idx,'format_type'] 			= 	t.ix[idx,header_row[3]].str.replace(r'[\s]*\|.*','')
		# -- first word
		idx 								= 	t[ t[header_row[3]].str.split().map(lambda s: False if not s or not formats_lower.count(s[0].lower()) else True) ].index
		t.ix[idx,'format_type'] 			= 	t.ix[idx,header_row[3]].str.split().map(lambda s: s[0])

		# -- REMOVE FORMAT values after identifying 'format_type'
		idx 								= 	t[t.format_type!=''].index
		t.ix[idx,header_row[3]] 			= 	''

		# -- repeatable tags with (enumerated | string | null)
		repeat_idx 							= 	t[ (t[header_row[3]].str.contains('repeatable',case=False)==True) ].index
		tmp 								= 	t.ix[repeat_idx,:]
		repeat_enumerated 					=	tmp[ (tmp[header_row[4]].str.startswith('(')==True) 
													& (tmp[header_row[4]].str.endswith(')')==True) ].index.tolist()
		repeat_string 						=	tmp[ (tmp[header_row[4]]!='') 
													& (tmp[header_row[4]].str.startswith('(')==False) ].index.tolist()
		repeat_empty 						= 	tmp[ tmp[header_row[4]]==''].index.tolist()
		assert len(repeat_idx)			   ==	len(repeat_enumerated)+len(repeat_string)+len(repeat_empty)
		
		# -- repeatable: enumerated
		if repeat_enumerated:
			rep_enumerated_idx_vals 		=	t.ix[repeat_enumerated,header_row[4]].tolist()
			_from_cols 						=	[header_row[3],header_row[4],'repeatable','format_type']
			_to_cols 						= 	[]
			for it in rep_enumerated_idx_vals:
				_to_cols.append(				['',it,True,'Enumerated'])
			t.ix[repeat_enumerated,_from_cols] 	= 	_to_cols

		# -- repeatable: string
		if repeat_string:
			rep_str_idx_vals 				= 	t.ix[repeat_string,header_row[4]].tolist()
			_from_cols 						=	[header_row[3],header_row[4],'repeatable','format_type']
			_to_cols 						= 	[]
			for it in rep_str_idx_vals:
				_to_cols.append(				['',it,True,'String'])
			t.ix[repeat_string,_from_cols] 	= 	_to_cols

		# -- repeatable: null
		if repeat_empty:
			t.ix[repeat_empty,header_row[3]]= 	''

		# Determine formats based on tag types
		t['description'] 					=	''

		format_by_tag 						= 	{'date'						:	{'Date':'YYYY-MM-DD'},
												 'time'						:	{'Time':'HH:mm'},
												 'year'						:	{'Date':'YYYY'},
												 'zipcode'					:	{'Integer':'00000'},
												 'phone' 					:	{'Integer':'000-000-0000'},
												 'state'					:	{'String':'XX'},
												 'price'					:	'Decimal',
												 'website'					:	'URL',
												 'id'						:	'Integer',
												 'name'						:	'String',
												 'number'					:	'Integer',
												 'url'						:	'URL',
												 'address'					:	'String',
												 #'code'						:	'Integer',
												 'email'					:	'Email',
												 'title'					:	'String',
												 'description'				:	'String',
												 }
		tmp 								= 	t[t[header_row[3]]!='']
		format_by_tag_keys 					= 	format_by_tag.keys()
		for k,v in tmp.iterrows():
			for it in format_by_tag_keys:
				if self.T.re_findall(r'[<]*[-]*%s[-]*[/]*' % it,v.element_name):
					t.ix[k,[header_row[3],'format_type']] = ['',format_by_tag[it]]
					break

		# Left Overs
		only_desc_idx 						= 	t[ (t[header_row[3]]!='') & (t[header_row[3]].str.startswith('|'))].index.tolist()
		t.ix[only_desc_idx,'description'] 	=	t.ix[only_desc_idx,header_row[3]].str.strip('| ')
		t.ix[only_desc_idx,header_row[3]] 	= 	''

		idx  								= 	t[t[header_row[3]]!=''].index.tolist()
		t.ix[idx,'description'] 			= 	t.ix[idx,header_row[3]]
		t.ix[idx,'format_type'] 			= 	'String'
		t.ix[idx,header_row[3]] 			= 	''
		
		t 									= 	t.drop(header_row[3],axis=1)
		
		# Clean up rows that included header cols (due to page breaks)
		t[header_row[4]] 					= 	t[header_row[4]].str.replace(r'RequiredTierFormat.*$','')
		
		# Make Lists for Options
		t['opts'] 							= 	''

		# -- enumerated
		enumerated_idx 						= 	t[t.format_type=='Enumerated'].index.tolist()
		_to_cols 							= 	[]
		for i in enumerated_idx:
			opts 							= 	[it.strip() for it in t.ix[i,header_row[4]].strip('() ').split('|')]
			_to_cols.append(					['',set(opts)])
		t.ix[enumerated_idx,[header_row[4],'opts']] = _to_cols

		# -- boolean
		boolean_idx 						= 	t[t.format_type=='Boolean'].index.tolist()
		_to_cols 							= 	[]
		for i in boolean_idx:
			opts 							= 	[it.strip() for it in t.ix[i,header_row[4]].strip('() ').split('|')]
			_to_cols.append(					['',set(opts)])
		
		t.ix[boolean_idx,[header_row[4],'opts']] = _to_cols

		# -- recommended
		recommended_idx						= 	t[t.format_type=='Recommended'].index.tolist()
		_to_cols 							= 	[]
		for i in recommended_idx:
			opts 							= 	[it.strip() for it in t.ix[i,header_row[4]].strip('() ').split('|')]
			_to_cols.append(					['',set(opts)])
		t.ix[recommended_idx,[header_row[4],'opts']] = _to_cols

		t['opts'] 							=	t['opts'].map(lambda f: '' if not f else tuple(f))

		# Create Example Column
		t['example'] 						= 	t[header_row[4]]
		take_cols 							= 	['element_name','required','tier','depth','container','repeatable',
												 'description','format_type','opts','example']
		
		t 									= 	t.ix[:,take_cols]
		t['format_type'] 					= 	t.format_type.map(lambda f: self.T.j_dump(f) if type(f) is dict else '' if not f else self.T.j_dump({f:''}))
		return t
		
	def save_feed_config_as_json(self,j_path='trulia_feed_config.json'):
		feed_config 						= 	self.scrape_feed_data()
		feed_config.to_json(					j_path)
		return True

	def load_feed_config_from_json(self,j_path='trulia_feed_config.json'):
		feed_config 						= 	self.T.pd.read_json(j_path).reset_index(drop=True)
		return feed_config
		
	