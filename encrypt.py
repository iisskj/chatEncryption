# encrypt.py —— 支持中英文

import random

# 英文替换表
EN_SYMBOLS = {'a': '@', 'e': '&', 'i': '!', 'o': '0', 'u': 'µ', 's': '$', 't': '+'}
DE_SYMBOLS = {v: k for k, v in EN_SYMBOLS.items()}

# 中文加密：Unicode 位移（避开控制字符）
CH_SHIFT = 3

def encrypt(text):
    words = text.split()
    if not words:
        return ""

    encrypted_parts = []
    for idx, word in enumerate(words):
        # 判断是否纯中文（或其他非英文）
        if word.isascii():
            # 英文或符号：走原加密流程
            clean = ''.join(c for c in word if c.isalpha())
            punct = ''.join(c for c in word if not c.isalpha())

            if clean:
                # 凯撒加密英文
                caesar = ""
                for c in clean.lower():
                    if c.isalpha():
                        shifted = (ord(c) - ord('a') + 3) % 26
                        caesar += chr(shifted + ord('a'))
                    else:
                        caesar += c
                # 符号替换
                substituted = ''.join(EN_SYMBOLS.get(c, c) for c in caesar)
                encrypted_word = substituted + punct
            else:
                encrypted_word = word
        else:
            # 中文或混合：直接 Unicode 位移
            encrypted_word = ""
            for c in word:
                encrypted_word += chr(ord(c) + CH_SHIFT)
            punct = ""

        # 添加位置标记（¤隐藏）
        encrypted_parts.append(encrypted_word + '¤' + str(idx))

    # 打乱词块顺序
    random.shuffle(encrypted_parts)
    return ' '.join(encrypted_parts)


def decrypt(cipher):
    if not cipher:
        return ""
    parts = cipher.split()
    result = [''] * len(parts)

    for part in parts:
        if '¤' not in part:
            continue
        content, pos_str = part.rsplit('¤', 1)
        if not pos_str.isdigit():
            continue
        pos = int(pos_str)

        # 判断是否含高位 Unicode（可能是中文）
        has_high_char = any(ord(c) > 128 for c in content)

        if has_high_char:
            # 中文解密：Unicode 逆位移
            decoded = ""
            for c in content:
                decoded += chr(ord(c) - CH_SHIFT)
            result[pos] = decoded
        else:
            # 英文解密
            clean_enc = ''.join(c for c in content if c.isalpha() or c in EN_SYMBOLS.values())
            punct = ''.join(c for c in content if not (c.isalpha() or c in EN_SYMBOLS.values()))
            substituted = ''.join(DE_SYMBOLS.get(c, c) for c in clean_enc)
            plain = ""
            for c in substituted:
                if c.isalpha():
                    shifted = (ord(c) - ord('a') - 3) % 26
                    plain += chr(shifted + ord('a'))
                else:
                    plain += c
            result[pos] = plain + punct

    return ' '.join(result)
