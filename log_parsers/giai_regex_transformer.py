import re
import sys
import yaml

G_GIAI_PATTERNS_GITHUB_URL = "https://raw.githubusercontent.com/aerospike/agi-stack/refs/heads/main/ingest/app/patterns.yml?token=GHSAT0AAAAAAB4VMHQ4M4XT45OA267N4CBQZX2JMYA"

# local patterns file
G_GIAI_DOWNLOADED_PATTERNS_FILENAME="configs/patterns.yml"
G_TOOL_LOG_FILENAME="process_output.log"

G_LOCAL_GIAI_REGEX_FILENAME="configs/giai_regex_patterns.txt"
G_MODIFIED_GIAI_REGEX_FILENAME="configs/modified_giai_regex_patterns.txt"
G_FLUENTBIT_MASTER_CONF_FILENAME="configs/fluentbit/master-fluent-bit-partial.conf"
G_FLUENTBIT_FILTER_SECTIONS_CONF_FILE="configs/fluentbit/fluent-bit-filters-section.conf"
G_FLUENTBIT_PARSERS_CONF_FILE="configs/fluentbit/fluent-bit-aerospike-parsers.conf"
G_SPLUNK_PROPS_CONF_FILE="configs/splunk/splunk_local_props.conf"
G_SPLUNK_TRANSFORMERS_CONF_FILE="configs/splunk/splunk_local_transforms.conf"

giai_unique_regex_set = set()
unique_regex_set = set()

# global regex to count words
g_word_pattern = re.compile(r'\w+')

# BEGIN fluent-bit parsers.conf and filter.conf generation
def read_fluentbit_conf_sections(): 
    conf_lines = ""
    with open(G_FLUENTBIT_MASTER_CONF_FILENAME) as fp:
        Lines = fp.readlines()
        for line in Lines:
            conf_lines = conf_lines + line
            
    return conf_lines

def construct_fluentbit_all_filters_prefix(filter_details):
    s= ""
    s= s+ "[FILTER]\n"
    s= s+ "    Name          parser\n"
    s= s+ "    Match         aero_logs*\n"
    s= s+ "    Key_Name      log\n"
    s= s+ filter_details
    s= s+ "    Reserve_data true\n"
    s= s+ "    Preserve_Key On\n"
    
    return s

def construct_fluent_output_sections():
    s= ""
    s= s + "[OUTPUT]\n"
    s= s + "    Name stdout\n"
    s= s + "    Match *\n"


    s= s + "[OUTPUT]\n"
    s= s + "    match *\n"
    s= s + "    name es\n"
    s= s + "    Host ${ELASTIC_HOSTNAME}\n"
    s= s + "    HTTP_User ${ELASTIC_USERNAME}\n"
    s= s + "    HTTP_Passwd ${ELASTIC_PASSWORD}\n"
    s= s + "    Port 9200\n"
    s= s + "    tls On\n"
    s= s + "    tls.verify Off\n"
    s= s + "    Suppress_Type_Name On\n"
    s= s + "    Index ${ELASTIC_INDEX_NAME}\n"
    s= s + "    Type _doc\n"
    s= s + "    Include_Tag_Key On\n"
    s= s + "    Tag_Key _tag\n"
    
    return s

def construct_fluentbit_filters_from_giai():
    read_modified_giai_regexs() 
     
    idx=0      
    individual_filters = ""
    all_filters_together=""
    all_parser_line=""
    
    for line in unique_regex_set:
        idx = idx +1
        l = line.replace("?P","?")
        f= ""
        f= f+ "[FILTER]\n"
        f= f+ "    Name parser\n"
        f= f+ "    Match aero_logs*\n"
        f= f+ "    Key_Name log\n"
        f= f+ "    Parser aero_log_parser_type_"+ str(idx)+"\n"
        f= f+ "    Reserve_Data true\n"
        f= f+ "    Preserve_Key On\n"
        
        p= ""
        p= p+ "[PARSER]\n"
        p= p+ "    # Aerospike RegEx patterns - "+str(idx)+" \n"
        p= p+ "    Name aero_log_parser_type_"+str(idx)+"\n"
        p= p+ "    Format regex\n"
        p= p+ "    Regex   "+ l+"\n"
        p= p+ "    Time_Key    datetime\n"        
        
        all_filters_together = all_filters_together + "    Parser aero_log_parser_type_"+ str(idx)+"\n"        
        # individual_filters = individual_filters + f + "\n"
        all_parser_line = all_parser_line+ p + "\n"
        
    
    return all_filters_together, individual_filters, all_parser_line
    
def construct_fluentbit_record_modifier():
    record_modifier_filter=""
    
    record_modifier_filter= record_modifier_filter+ "[FILTER]\n"
    record_modifier_filter= record_modifier_filter+ "    Name record_modifier\n"
    record_modifier_filter= record_modifier_filter+ "    Match *\n"
    record_modifier_filter= record_modifier_filter+ "    Record cluster_name ${CLUSTER_NAME} \n"
    record_modifier_filter= record_modifier_filter+ "    Record hostname ${HOSTNAME}\n"
    
    return record_modifier_filter

def generate_fluentbit_conf_files(): 
    # clean-up global sets/lists
    unique_regex_set.clear()
    giai_unique_regex_set.clear()
           
    individual_filters = ""
    all_fluent_bit_configs= ""    
    all_filters_together=""
    output_sections=""        
    record_modifier_filter=""
    all_parser_lines = ""
    fluentbit_conf_sections=""
    
    record_modifier_filter= construct_fluentbit_record_modifier()    
    all_filters_together, individual_filters, all_parser_lines = construct_fluentbit_filters_from_giai()    
    all_filters_together = construct_fluentbit_all_filters_prefix(all_filters_together)
    output_sections = output_sections + construct_fluent_output_sections()
    
    all_fluent_bit_configs = all_fluent_bit_configs + individual_filters+"\n"
    all_fluent_bit_configs = all_fluent_bit_configs + record_modifier_filter+"\n"
    all_fluent_bit_configs = all_fluent_bit_configs + all_filters_together+"\n"

    # Add the SERVICE section    
    # fluentbit_conf_sections= read_fluentbit_conf_sections()
    # Add output section
    # all_fluent_bit_configs = all_fluent_bit_configs + output_sections+"\n"
    
    fh_fluentbit_conf = open(G_FLUENTBIT_FILTER_SECTIONS_CONF_FILE, "w")
    fh_fluentbit_conf.write(fluentbit_conf_sections+"\n")    
    fh_fluentbit_conf.write(all_fluent_bit_configs+"\n")
    fh_fluentbit_conf.close()    

    fh_fluentbit_parser_conf = open(G_FLUENTBIT_PARSERS_CONF_FILE, "w")
    fh_fluentbit_parser_conf.write(all_parser_lines)
    fh_fluentbit_parser_conf.close()    

# END fluent-bit parsers.conf and filter.conf generation

# BEGIN splunk props.conf and transform.conf generation
    
def construct_splunk_regex_fields_from_regex(p_regex):
    idx = 0
    group_names = re.findall(r"\?P<(\w+)>", p_regex)
    field_names = ""
    for l in group_names:
        idx = idx + 1
        field_names = str(field_names).lower()+l+"::$"+str(idx)+" "
    
    return field_names.strip(" ")

def construct_splunk_transform_stanza(p_stanza_id, p_regex):
    stanza = ""
    stanza = stanza + "["+p_stanza_id +"]" + "\n"
    # stanza = stanza + "REGEX = " + str(p_regex).lower() + "\n"
    # l_regex = convert_group_names_to_lower(p_regex)
    l_regex = p_regex
    stanza = stanza + "REGEX = " + l_regex + "\n"
    stanza = stanza + "FORMAT = " + construct_splunk_regex_fields_from_regex(l_regex) + "\n"
    
    return stanza

def generate_splunk_conf_files():
    unique_regex_set.clear()
    
    read_modified_giai_regexs()
    idx=0
    transform_stanzas = ""
    props_stanzas="[aerospike]" + "\n"
    
    for line in unique_regex_set:
        idx = idx +1
        
        if not "#" in line:
            stanza_id = "aero_log_parser_type_"+str(idx)
            props_stanzas = props_stanzas +"REPORT-"+stanza_id+" = " + stanza_id + "\n"
            transform_stanzas = transform_stanzas + construct_splunk_transform_stanza( stanza_id, line) +"\n"       
    
    # save to transform.conf file
    fh_splunk_transform_conf = open(G_SPLUNK_TRANSFORMERS_CONF_FILE, "w")
    fh_splunk_transform_conf.write(transform_stanzas)    
    fh_splunk_transform_conf.close()    

    fh_splunk_props_conf = open(G_SPLUNK_PROPS_CONF_FILE, "w")
    fh_splunk_props_conf.write(props_stanzas)    
    fh_splunk_props_conf.close()    
       
# END splunk props.conf and transform.conf generation              

# commons functions

def check_valid_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error as e:
        return False

def check_if_parsable_regex(pattern):
    word_count = g_word_pattern.findall(pattern)
    return (len(word_count)>2)

def convert_group_names_to_lower(p_regex):
    group_names = re.findall(r'\?P<(\w+)>', p_regex)    
    lowercase_map = {name: name.lower() for name in group_names}
    l_regex = str( p_regex)
    for orig_name, lower_name in lowercase_map.items():
        l_regex = l_regex.replace( orig_name, lower_name)
        # l_regex = re.sub(r'\?P<{}>'.format(orig_name), r'(?P<{}>'.format(lower_name), l_regex)

    return l_regex

def read_modified_giai_regexs(): 
    with open(G_MODIFIED_GIAI_REGEX_FILENAME) as fp:
        Lines = fp.readlines()
        for line in Lines:
            if not line.startswith("#"): 
                unique_regex_set.add( line.strip())

def get_patterns_file_from_github():
    import os
    import shutil
    use_local_patterns = os.environ.get("USE_LOCAL_PATTERNS_FILE")
    if len(use_local_patterns.strip())>0:
        print("Using local patterns file ... ")
        shutil.copyfile(G_LOCAL_GIAI_REGEX_FILENAME, G_GIAI_DOWNLOADED_PATTERNS_FILENAME)    
    else:
        import urllib.request
        print("Downloading patterns.yml from GitHub aerospike/agi_stack repo . ")
        downloaded_fileloc, http_msg= urllib.request.urlretrieve (G_GIAI_PATTERNS_GITHUB_URL)
        shutil.copyfile(downloaded_fileloc, G_GIAI_DOWNLOADED_PATTERNS_FILENAME)    

def parse_patterns_yaml():
    with open(G_GIAI_DOWNLOADED_PATTERNS_FILENAME, "r") as fh:
        data = yaml.safe_load(fh)
        patterns = (data.get("patterns"))
        unique_regex_str = ""
        ignored_line_str = ""
        for item in patterns:
            for rex in item["export"]:
                output, is_valid=parse_export_regex(rex)
                if is_valid:
                    unique_regex_str = unique_regex_str + output +"\n"
                else:
                    ignored_line_str = ignored_line_str + output +"\n"         
                
        # save to modified patterns to file
        fh_modified_pattterns_conf = open(G_MODIFIED_GIAI_REGEX_FILENAME, "w")
        fh_modified_pattterns_conf.write(unique_regex_str)    
        fh_modified_pattterns_conf.close()  
        # print( unique_regex_str)  
        
        # sace output log
        fh_modified_pattterns_conf = open(G_TOOL_LOG_FILENAME, "w")
        fh_modified_pattterns_conf.write(ignored_line_str)    
        fh_modified_pattterns_conf.close()  

def parse_export_regex(p_regex):
    l = p_regex
    # remove leading / trailing spaces
    l = l.strip() 
    ret_reg = p_regex
    
    if  not l.startswith("#") : 
        l = l.replace("\"","")
        l = l.replace("\\(","(")
        l = l.replace("\\)",")")
        l = l.replace("\\\d","\\d")
        l = l.replace("\\\(","\\(")
        l = l.replace("\\\)","\)")        
        l = l.replace("\\[","[")        
        l = l.replace("\\]","]")        

        # if there is a comment in between the regex, pick only the regex and ignore the rest of comments
        if "#" in l:
            l= l[:p_regex.find("#")-2]
            l= l.strip(" ")
        
        # remove leading hypen (-)
        # print(l)
        # l= l[1:]
        # l= l.strip(" ")
            
        if check_if_parsable_regex(l):
            ret_reg = "^(?P<datetimestamp>\w+ \d+ \d+ \d+:\d+:\d+) (?P<timezone>\S+): (?P<log_level>\S+) \((?P<source>\S+)\): \((?P<source_location>[^)]+)\)\s+"+ l + "$"
            
            if check_valid_regex( p_regex):
                unique_regex_str = "# Giai line ==> "+p_regex +"\n"
                unique_regex_str = unique_regex_str + ret_reg 
                unique_regex_set.add ("# Giai line ==> "+p_regex)           
                unique_regex_set.add (ret_reg)
                
                return unique_regex_str, True
            else:
                ret_reg = "# Giai line, Ignoring, invalid regex syntax issues ==> "+p_regex 
                return ret_reg, False
        else:
            ret_reg = "# Giai line, Ignoring, invalid regex is very small ==> "+p_regex 
            return ret_reg, False
            
    else:
        ret_reg = "# Giai line, Ignoring ==> "+p_regex
    
    return ret_reg, False
    
    
# end common functions

if __name__ == '__main__':
    is_fluent_bit_conf= False
    is_splunk_conf= False
    
    print("Usage: python3 giai_regex_transformer.py <Optional: tool-name>")
    print("\t tool-name supported values: all,fluentbit, splunk ")
    
    # no conf, both fluent-bit and splunk
    # 
    # first-arg is always python scriptname, i.e. sys.argv[0] is giai_regex_transformer.py
    if len(sys.argv)==1 or sys.argv[1].lower()=="all":
        is_fluent_bit_conf=True
        is_splunk_conf=True
    elif sys.argv[1].lower()=="fluentbit":
        is_fluent_bit_conf=True
    elif sys.argv[1].lower()=="splunk":
        is_splunk_conf=True
        
    # download file from GitHub into config/patterns.txt
    # 
    get_patterns_file_from_github()
    parse_patterns_yaml()    

    if is_fluent_bit_conf==True:    
       generate_fluentbit_conf_files()
       
    if is_splunk_conf==True:    
       generate_splunk_conf_files()
    
