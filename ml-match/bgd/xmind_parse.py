from xmindparser import xmind_to_json
import json


def convert_xmind2json(in_xmind_file):
    # save JSON to the save path of in_xmind_file
    # but the context of CN is Unicode
    out_file = xmind_to_json(in_xmind_file)
    print(out_file)

    with open(out_file, 'r') as f:
        unicode_content = f.read()
        print(unicode_content)
        # convert to CN
        normal_json = json.loads(unicode_content, encoding='utf-8')
        print(normal_json)

        with open("normal.json", 'w') as w_f:
            w_f.write(json.dumps(normal_json, ensure_ascii=False))


if __name__ == '__main__':
    xmind_file = 'C:\\Users\\DELL\\Documents\\WeChat Files\\zengxijin\\Files\\智能推荐0219.xmind'
    convert_xmind2json(xmind_file)

