from re import sub

def rle_decode(s: str):
	return sub(r'(\d+)(\D)', lambda m: m.group(2) * int(m.group(1)), s)