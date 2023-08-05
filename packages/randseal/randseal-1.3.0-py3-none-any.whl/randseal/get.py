import discord, random
from importlib import resources

def file(num: int=None):
	"""
	Returns a `discord.File()` of a seal for py-cord
	"""
	if num == None:
		sealrand = f"{random.randrange(1, 82)}"
	else: 
		if not sealrand > 82:
			sealrand = num
		else:
			sealrand = f"{random.randrange(1, 82)}"
	if len(sealrand) == 1:
		sussy = sealrand
		sealrand = "0" + f"{sussy}"
	with resources.open_text('randseal', f'00{sealrand}.jpg') as fp:
		return discord.File(fp=fp.name, filename=f"{sealrand}.png")

def embed(num: int=None, title: str="** **"):
	"""
	Returns a `discord.Embed()` of a seal
	"""
	if num == None:
		sealrand = f"{random.randrange(1, 82)}"
	else: 
		if not sealrand > 82:
			sealrand = num
		else:
			sealrand = f"{random.randrange(1, 82)}"
	if len(sealrand) == 1:
		sussy = sealrand
		sealrand = "0" + f"{sussy}"
	embeda = discord.Embed(colour=0x2f3136, title=title).set_image(url=f"https://raw.githubusercontent.com/mariohero24/randseal/main/randseal/00{sealrand}.jpg")
	return embeda