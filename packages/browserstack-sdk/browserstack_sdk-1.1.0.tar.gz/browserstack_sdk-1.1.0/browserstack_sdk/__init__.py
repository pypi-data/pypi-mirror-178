# coding: UTF-8
import sys
bstack1ll_opy_ = sys.version_info [0] == 2
bstack1l11_opy_ = 2048
bstack11_opy_ = 7
def bstackl_opy_ (bstack1lll_opy_):
    global bstack1ll1_opy_
    bstack1l1l_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l1_opy_ = bstack1lll_opy_ [:-1]
    bstack1_opy_ = bstack1l1l_opy_ % len (bstack1l1_opy_)
    bstack111_opy_ = bstack1l1_opy_ [:bstack1_opy_] + bstack1l1_opy_ [bstack1_opy_:]
    if bstack1ll_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11_opy_ - (bstack11l_opy_ + bstack1l1l_opy_) % bstack11_opy_) for bstack11l_opy_, char in enumerate (bstack111_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1l11_opy_ - (bstack11l_opy_ + bstack1l1l_opy_) % bstack11_opy_) for bstack11l_opy_, char in enumerate (bstack111_opy_)])
    return eval (bstack1l_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
from packaging import version
from browserstack.local import Local
bstack11l1_opy_ = {
	bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨन"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࠫऩ"),
  bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫप"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡭ࡨࡽࠬफ"),
  bstackl_opy_ (u"ࠪࡳࡸ࠭ब"): bstackl_opy_ (u"ࠫࡴࡹࠧभ"),
  bstackl_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨम"): bstackl_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪय"),
  bstackl_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧर"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨऱ"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧल"): bstackl_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࠫळ"),
  bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧऴ"): bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫव"),
  bstackl_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫश"): bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬष"),
  bstackl_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧस"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭ࠧह"),
  bstackl_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨऺ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡳࡰ࡮ࡨࠫऻ"),
  bstackl_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵ़ࠪ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪऽ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫा"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫि"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨी"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡹ࡭ࡩ࡫࡯ࠨु"),
  bstackl_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪू"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪृ"),
  bstackl_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ॄ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ॅ"),
  bstackl_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ॆ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭े"),
  bstackl_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬै"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸ࡮ࡳࡥࡻࡱࡱࡩࠬॉ"),
  bstackl_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩॊ"): bstackl_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪो"),
  bstackl_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩौ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰ्ࠪ"),
  bstackl_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨॎ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨॏ"),
  bstackl_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩॐ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩ॑"),
  bstackl_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭॒࠭"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭॓"),
  bstackl_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪ॔"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡲࡩࡑࡥࡺࡵࠪॕ"),
  bstackl_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬॖ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬॗ"),
  bstackl_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫक़"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡶࠫख़"),
  bstackl_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨग़"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡨࡦࡥࡨ࡮ࡥࠨज़"),
  bstackl_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪड़"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪढ़"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧफ़"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧय़"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪॠ"): bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧॡ"),
  bstackl_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬॢ"): bstackl_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧॣ"),
  bstackl_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ।"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ॥"),
  bstackl_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ०"): bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡕࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪ१"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ२"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ३"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ४"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ५"),
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ६"): bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭७"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ८"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ९"),
  bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ॰"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨॱ"),
}
bstack11ll_opy_ = [
  bstackl_opy_ (u"ࠪࡳࡸ࠭ॲ"),
  bstackl_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧॳ"),
  bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧॴ"),
  bstackl_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫॵ"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫॶ"),
  bstackl_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬॷ"),
  bstackl_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩॸ"),
]
bstack1l1ll_opy_ = {
  bstackl_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ॹ"): bstackl_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨॺ"),
  bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧॻ"): [bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨॼ"), bstackl_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪॽ")],
  bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ॾ"): bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧॿ"),
  bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧঀ"): bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫঁ"),
  bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪং"): [bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧঃ"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭঄")],
  bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩঅ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫআ"),
  bstackl_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧই"): bstackl_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩঈ"),
  bstackl_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬউ"): [bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ঊ"), bstackl_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨঋ")],
  bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧঌ"): [bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪ঍"), bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࠪ঎")]
}
bstack1l11l_opy_ = {
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪএ"): [bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ঐ"), bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭঑")]
}
bstack11lll_opy_ = [
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭঒"),
  bstackl_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫও"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨঔ"),
  bstackl_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶࠪক"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭খ"),
  bstackl_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻࠪগ"),
  bstackl_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩঘ")
]
bstack1l111_opy_ = [
  bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঙ"),
  bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬচ"),
  bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨছ"),
  bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪজ"),
  bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧঝ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧঞ"),
  bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩট"),
  bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫঠ"),
  bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫড"),
]
bstack1llll_opy_ = [
  bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ঢ"),
  bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩণ"),
]
bstack11ll1_opy_ = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡽࡤ࠰ࡪࡸࡦࠬত")
bstack11l1l_opy_ = bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠨথ")
bstack1ll11_opy_ = {
  bstackl_opy_ (u"࠭ࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠨদ"): 50,
  bstackl_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ধ"): 40,
  bstackl_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩন"): 30,
  bstackl_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ঩"): 20,
  bstackl_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩপ"): 10
}
DEFAULT_LOG_LEVEL = bstack1ll11_opy_[bstackl_opy_ (u"ࠫ࡮ࡴࡦࡰࠩফ")]
bstack1lll1_opy_ = bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫব")
bstack111l1_opy_ = bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫভ")
bstack111l_opy_ = [bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨম"), bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨয")]
bstack111ll_opy_ = [bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬর"), bstackl_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ঱")]
bstack1111_opy_ = [
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡏࡣࡰࡩࠬল"),
  bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ঳"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ঴"),
  bstackl_opy_ (u"ࠧ࡯ࡧࡺࡇࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࠫ঵"),
  bstackl_opy_ (u"ࠨࡣࡳࡴࠬশ"),
  bstackl_opy_ (u"ࠩࡸࡨ࡮ࡪࠧষ"),
  bstackl_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬস"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࠫহ"),
  bstackl_opy_ (u"ࠬࡵࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪ঺"),
  bstackl_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࠫ঻"),
  bstackl_opy_ (u"ࠧ࡯ࡱࡕࡩࡸ࡫ࡴࠨ়"), bstackl_opy_ (u"ࠨࡨࡸࡰࡱࡘࡥࡴࡧࡷࠫঽ"),
  bstackl_opy_ (u"ࠩࡦࡰࡪࡧࡲࡔࡻࡶࡸࡪࡳࡆࡪ࡮ࡨࡷࠬা"),
  bstackl_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡖ࡬ࡱ࡮ࡴࡧࡴࠩি"),
  bstackl_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࡍࡱࡪ࡫࡮ࡴࡧࠨী"),
  bstackl_opy_ (u"ࠬࡵࡴࡩࡧࡵࡅࡵࡶࡳࠨু"),
  bstackl_opy_ (u"࠭ࡰࡳ࡫ࡱࡸࡕࡧࡧࡦࡕࡲࡹࡷࡩࡥࡐࡰࡉ࡭ࡳࡪࡆࡢ࡫࡯ࡹࡷ࡫ࠧূ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳࡅࡨࡺࡩࡷ࡫ࡷࡽࠬৃ"), bstackl_opy_ (u"ࠨࡣࡳࡴࡕࡧࡣ࡬ࡣࡪࡩࠬৄ"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡄࡧࡹ࡯ࡶࡪࡶࡼࠫ৅"), bstackl_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡔࡦࡩ࡫ࡢࡩࡨࠫ৆"), bstackl_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ে"),
  bstackl_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪৈ"),
  bstackl_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙࡫ࡳࡵࡒࡤࡧࡰࡧࡧࡦࡵࠪ৉"),
  bstackl_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࠩ৊"), bstackl_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࡈࡲࡩࡏ࡮ࡵࡧࡱࡸࠬো"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧৌ"),
  bstackl_opy_ (u"ࠪࡥࡩࡨࡐࡰࡴࡷ্ࠫ"),
  bstackl_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡗࡴࡩ࡫ࡦࡶࠪৎ"),
  bstackl_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱ࡚ࡩ࡮ࡧࡲࡹࡹ࠭৏"),
  bstackl_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡶ࡫ࠫ৐"),
  bstackl_opy_ (u"ࠧࡢࡸࡧࠫ৑"), bstackl_opy_ (u"ࠨࡣࡹࡨࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫ৒"), bstackl_opy_ (u"ࠩࡤࡺࡩࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫ৓"), bstackl_opy_ (u"ࠪࡥࡻࡪࡁࡳࡩࡶࠫ৔"),
  bstackl_opy_ (u"ࠫࡺࡹࡥࡌࡧࡼࡷࡹࡵࡲࡦࠩ৕"), bstackl_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡶ࡫ࠫ৖"), bstackl_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡶࡷࡼࡵࡲࡥࠩৗ"),
  bstackl_opy_ (u"ࠧ࡬ࡧࡼࡅࡱ࡯ࡡࡴࠩ৘"), bstackl_opy_ (u"ࠨ࡭ࡨࡽࡕࡧࡳࡴࡹࡲࡶࡩ࠭৙"),
  bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫ৚"), bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡃࡵ࡫ࡸ࠭৛"), bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪࡊࡩࡳࠩড়"), bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡇ࡭ࡸ࡯࡮ࡧࡐࡥࡵࡶࡩ࡯ࡩࡉ࡭ࡱ࡫ࠧঢ়"), bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶ࡚ࡹࡥࡔࡻࡶࡸࡪࡳࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪ৞"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࠪয়"), bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࡷࠬৠ"),
  bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡅ࡫ࡶࡥࡧࡲࡥࡃࡷ࡬ࡰࡩࡉࡨࡦࡥ࡮ࠫৡ"),
  bstackl_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࡕ࡫ࡰࡩࡴࡻࡴࠨৢ"),
  bstackl_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡅࡨࡺࡩࡰࡰࠪৣ"), bstackl_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡈࡧࡴࡦࡩࡲࡶࡾ࠭৤"), bstackl_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡌ࡬ࡢࡩࡶࠫ৥"), bstackl_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡡ࡭ࡋࡱࡸࡪࡴࡴࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ০"),
  bstackl_opy_ (u"ࠨࡦࡲࡲࡹ࡙ࡴࡰࡲࡄࡴࡵࡕ࡮ࡓࡧࡶࡩࡹ࠭১"),
  bstackl_opy_ (u"ࠩࡸࡲ࡮ࡩ࡯ࡥࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫ২"), bstackl_opy_ (u"ࠪࡶࡪࡹࡥࡵࡍࡨࡽࡧࡵࡡࡳࡦࠪ৩"),
  bstackl_opy_ (u"ࠫࡳࡵࡓࡪࡩࡱࠫ৪"),
  bstackl_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩ࡚ࡴࡩ࡮ࡲࡲࡶࡹࡧ࡮ࡵࡘ࡬ࡩࡼࡹࠧ৫"),
  bstackl_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯ࡦࡵࡳ࡮ࡪࡗࡢࡶࡦ࡬ࡪࡸࡳࠨ৬"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৭"),
  bstackl_opy_ (u"ࠨࡴࡨࡧࡷ࡫ࡡࡵࡧࡆ࡬ࡷࡵ࡭ࡦࡆࡵ࡭ࡻ࡫ࡲࡔࡧࡶࡷ࡮ࡵ࡮ࡴࠩ৮"),
  bstackl_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ৯"),
  bstackl_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡐࡢࡶ࡫ࠫৰ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡘࡶࡥࡦࡦࠪৱ"),
  bstackl_opy_ (u"ࠬ࡭ࡰࡴࡇࡱࡥࡧࡲࡥࡥࠩ৲"),
  bstackl_opy_ (u"࠭ࡩࡴࡊࡨࡥࡩࡲࡥࡴࡵࠪ৳"),
  bstackl_opy_ (u"ࠧࡢࡦࡥࡉࡽ࡫ࡣࡕ࡫ࡰࡩࡴࡻࡴࠨ৴"),
  bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࡔࡥࡵ࡭ࡵࡺࠧ৵"),
  bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡄࡦࡸ࡬ࡧࡪࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭৶"),
  bstackl_opy_ (u"ࠪࡥࡺࡺ࡯ࡈࡴࡤࡲࡹࡖࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠪ৷"),
  bstackl_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡓࡧࡴࡶࡴࡤࡰࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ৸"),
  bstackl_opy_ (u"ࠬࡹࡹࡴࡶࡨࡱࡕࡵࡲࡵࠩ৹"),
  bstackl_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡤࡣࡊࡲࡷࡹ࠭৺"),
  bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴ࡚ࡴ࡬ࡰࡥ࡮ࠫ৻"), bstackl_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡕࡻࡳࡩࠬৼ"), bstackl_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡍࡨࡽࠬ৽"),
  bstackl_opy_ (u"ࠪࡥࡺࡺ࡯ࡍࡣࡸࡲࡨ࡮ࠧ৾"),
  bstackl_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡨࡧࡴࡄࡣࡳࡸࡺࡸࡥࠨ৿"),
  bstackl_opy_ (u"ࠬࡻ࡮ࡪࡰࡶࡸࡦࡲ࡬ࡐࡶ࡫ࡩࡷࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧ਀"),
  bstackl_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡗࡪࡰࡧࡳࡼࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࠨਁ"),
  bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚࡯ࡰ࡮ࡶ࡚ࡪࡸࡳࡪࡱࡱࠫਂ"),
  bstackl_opy_ (u"ࠨࡧࡱࡪࡴࡸࡣࡦࡃࡳࡴࡎࡴࡳࡵࡣ࡯ࡰࠬਃ"),
  bstackl_opy_ (u"ࠩࡨࡲࡸࡻࡲࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡵࡋࡥࡻ࡫ࡐࡢࡩࡨࡷࠬ਄"), bstackl_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡈࡪࡼࡴࡰࡱ࡯ࡷࡕࡵࡲࡵࠩਅ"), bstackl_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨ࡛ࡪࡨࡶࡪࡧࡺࡈࡪࡺࡡࡪ࡮ࡶࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠧਆ"),
  bstackl_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡶࡰࡴࡅࡤࡧ࡭࡫ࡌࡪ࡯࡬ࡸࠬਇ"),
  bstackl_opy_ (u"࠭ࡣࡢ࡮ࡨࡲࡩࡧࡲࡇࡱࡵࡱࡦࡺࠧਈ"),
  bstackl_opy_ (u"ࠧࡣࡷࡱࡨࡱ࡫ࡉࡥࠩਉ"),
  bstackl_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨਊ"),
  bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡊࡴࡡࡣ࡮ࡨࡨࠬ਋"), bstackl_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡇࡵࡵࡪࡲࡶ࡮ࢀࡥࡥࠩ਌"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰࡃࡦࡧࡪࡶࡴࡂ࡮ࡨࡶࡹࡹࠧ਍"), bstackl_opy_ (u"ࠬࡧࡵࡵࡱࡇ࡭ࡸࡳࡩࡴࡵࡄࡰࡪࡸࡴࡴࠩ਎"),
  bstackl_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡵࡏ࡭ࡧ࠭ਏ"),
  bstackl_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡗࡥࡵ࠭ਐ"),
  bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡰ࡬ࡸ࡮ࡧ࡬ࡖࡴ࡯ࠫ਑"), bstackl_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡃ࡯ࡰࡴࡽࡐࡰࡲࡸࡴࡸ࠭਒"), bstackl_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌ࡫ࡳࡵࡲࡦࡈࡵࡥࡺࡪࡗࡢࡴࡱ࡭ࡳ࡭ࠧਓ"), bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵ࡫࡮ࡍ࡫ࡱ࡯ࡸࡏ࡮ࡃࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧࠫਔ"),
  bstackl_opy_ (u"ࠬࡱࡥࡦࡲࡎࡩࡾࡉࡨࡢ࡫ࡱࡷࠬਕ"),
  bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࢀࡡࡣ࡮ࡨࡗࡹࡸࡩ࡯ࡩࡶࡈ࡮ࡸࠧਖ"),
  bstackl_opy_ (u"ࠧࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪਗ"),
  bstackl_opy_ (u"ࠨ࡫ࡱࡸࡪࡸࡋࡦࡻࡇࡩࡱࡧࡹࠨਘ"),
  bstackl_opy_ (u"ࠩࡶ࡬ࡴࡽࡉࡐࡕࡏࡳ࡬࠭ਙ"),
  bstackl_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡗࡹࡸࡡࡵࡧࡪࡽࠬਚ"),
  bstackl_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡖࡪࡹࡰࡰࡰࡶࡩ࡙࡯࡭ࡦࡱࡸࡸࠬਛ"), bstackl_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࡙ࡤ࡭ࡹ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ਜ"),
  bstackl_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࠩਝ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡴࡻࡱࡧࡊࡾࡥࡤࡷࡷࡩࡋࡸ࡯࡮ࡊࡷࡸࡵࡹࠧਞ"),
  bstackl_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡅࡤࡴࡹࡻࡲࡦࠩਟ"),
  bstackl_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩਠ"),
  bstackl_opy_ (u"ࠪࡪࡺࡲ࡬ࡄࡱࡱࡸࡪࡾࡴࡍ࡫ࡶࡸࠬਡ"),
  bstackl_opy_ (u"ࠫࡼࡧࡩࡵࡈࡲࡶࡆࡶࡰࡔࡥࡵ࡭ࡵࡺࠧਢ"),
  bstackl_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡉ࡯࡯ࡰࡨࡧࡹࡘࡥࡵࡴ࡬ࡩࡸ࠭ਣ"),
  bstackl_opy_ (u"࠭ࡡࡱࡲࡑࡥࡲ࡫ࠧਤ"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡔࡎࡆࡩࡷࡺࠧਥ"),
  bstackl_opy_ (u"ࠨࡶࡤࡴ࡜࡯ࡴࡩࡕ࡫ࡳࡷࡺࡐࡳࡧࡶࡷࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ਦ"),
  bstackl_opy_ (u"ࠩࡶࡧࡦࡲࡥࡇࡣࡦࡸࡴࡸࠧਧ"),
  bstackl_opy_ (u"ࠪࡻࡩࡧࡌࡰࡥࡤࡰࡕࡵࡲࡵࠩਨ"),
  bstackl_opy_ (u"ࠫࡸ࡮࡯ࡸ࡚ࡦࡳࡩ࡫ࡌࡰࡩࠪ਩"),
  bstackl_opy_ (u"ࠬ࡯࡯ࡴࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡹࡸ࡫ࠧਪ"),
  bstackl_opy_ (u"࠭ࡸࡤࡱࡧࡩࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠨਫ"),
  bstackl_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡷࡸࡽ࡯ࡳࡦࠪਬ"),
  bstackl_opy_ (u"ࠨࡷࡶࡩࡕࡸࡥࡣࡷ࡬ࡰࡹ࡝ࡄࡂࠩਭ"),
  bstackl_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶ࡚ࡈࡆࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪਮ"),
  bstackl_opy_ (u"ࠪࡻࡪࡨࡄࡳ࡫ࡹࡩࡷࡇࡧࡦࡰࡷ࡙ࡷࡲࠧਯ"),
  bstackl_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡵࡪࠪਰ"),
  bstackl_opy_ (u"ࠬࡻࡳࡦࡐࡨࡻ࡜ࡊࡁࠨ਱"),
  bstackl_opy_ (u"࠭ࡷࡥࡣࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩਲ"), bstackl_opy_ (u"ࠧࡸࡦࡤࡇࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࡔࡪ࡯ࡨࡳࡺࡺࠧਲ਼"),
  bstackl_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡏࡳࡩࡌࡨࠬ਴"), bstackl_opy_ (u"ࠩࡻࡧࡴࡪࡥࡔ࡫ࡪࡲ࡮ࡴࡧࡊࡦࠪਵ"),
  bstackl_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧ࡛ࡉࡇࡂࡶࡰࡧࡰࡪࡏࡤࠨਸ਼"),
  bstackl_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡒࡲࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡳࡶࡒࡲࡱࡿࠧ਷"),
  bstackl_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹࡹࠧਸ"),
  bstackl_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡩࡦࡵࠪਹ"), bstackl_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡺࡋࡱࡸࡪࡸࡶࡢ࡮ࠪ਺"),
  bstackl_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࡊࡤࡶࡩࡽࡡࡳࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫ਻"),
  bstackl_opy_ (u"ࠩࡰࡥࡽ࡚ࡹࡱ࡫ࡱ࡫ࡋࡸࡥࡲࡷࡨࡲࡨࡿ਼ࠧ"),
  bstackl_opy_ (u"ࠪࡷ࡮ࡳࡰ࡭ࡧࡌࡷ࡛࡯ࡳࡪࡤ࡯ࡩࡈ࡮ࡥࡤ࡭ࠪ਽"),
  bstackl_opy_ (u"ࠫࡺࡹࡥࡄࡣࡵࡸ࡭ࡧࡧࡦࡕࡶࡰࠬਾ"),
  bstackl_opy_ (u"ࠬࡹࡨࡰࡷ࡯ࡨ࡚ࡹࡥࡔ࡫ࡱ࡫ࡱ࡫ࡴࡰࡰࡗࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡸࠧਿ"),
  bstackl_opy_ (u"࠭ࡳࡵࡣࡵࡸࡎ࡝ࡄࡑࠩੀ"),
  bstackl_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚࡯ࡶࡥ࡫ࡍࡩࡋ࡮ࡳࡱ࡯ࡰࠬੁ"),
  bstackl_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡉ࡫ࡧࡨࡪࡴࡁࡱ࡫ࡓࡳࡱ࡯ࡣࡺࡇࡵࡶࡴࡸࠧੂ"),
  bstackl_opy_ (u"ࠩࡰࡳࡨࡱࡌࡰࡥࡤࡸ࡮ࡵ࡮ࡂࡲࡳࠫ੃"),
  bstackl_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉࡳࡷࡳࡡࡵࠩ੄"), bstackl_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊ࡮ࡲࡴࡦࡴࡖࡴࡪࡩࡳࠨ੅"),
  bstackl_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡈࡪࡲࡡࡺࡃࡧࡦࠬ੆")
]
bstack11l11_opy_ = bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡻࡰ࡭ࡱࡤࡨࠬੇ")
bstack1ll1l_opy_ = [bstackl_opy_ (u"ࠧ࠯ࡣࡳ࡯ࠬੈ"), bstackl_opy_ (u"ࠨ࠰ࡤࡥࡧ࠭੉"), bstackl_opy_ (u"ࠩ࠱࡭ࡵࡧࠧ੊")]
bstack1l1l1_opy_ = [bstackl_opy_ (u"ࠪ࡭ࡩ࠭ੋ"), bstackl_opy_ (u"ࠫࡵࡧࡴࡩࠩੌ"), bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ੍"), bstackl_opy_ (u"࠭ࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࠬ੎")]
bstack111lll_opy_ = bstackl_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠽ࠤࢀࢃࠧ੏")
bstack1l1111_opy_ = bstackl_opy_ (u"ࠨࡅࡲࡱࡵࡲࡥࡵࡧࡧࠤࡸ࡫ࡴࡶࡲࠤࠫ੐")
bstack11lll1_opy_ = bstackl_opy_ (u"ࠩࡓࡥࡷࡹࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫੑ")
bstack1ll1ll1_opy_ = bstackl_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧ੒")
bstack11ll1l1_opy_ = bstackl_opy_ (u"ࠫࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࡽࢀࠫ੓")
bstack1l1l1111_opy_ = bstackl_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡪࡰࡷࡩࡷࡸࡵࡱࡶ࠯ࠤࡪࡾࡩࡵ࡫ࡱ࡫ࠬ੔")
bstack11l1111_opy_ = bstackl_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫ੕")
bstack1l1l111l_opy_ = bstackl_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡴࡲࡦࡴࡺࠬࠡࡲࡤࡦࡴࡺࠠࡢࡰࡧࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡲࡩࡣࡴࡤࡶࡾࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡶࡲࠤࡷࡻ࡮ࠡࡴࡲࡦࡴࡺࠠࡵࡧࡶࡸࡸࠦࡩ࡯ࠢࡳࡥࡷࡧ࡬࡭ࡧ࡯࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠳ࡰࡢࡤࡲࡸࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࡡࠩ੖")
bstack1l1lll_opy_ = bstackl_opy_ (u"ࠨࡊࡤࡲࡩࡲࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡲ࡯ࡴࡧࠪ੗")
bstack1l1l1lll_opy_ = bstackl_opy_ (u"ࠩࡄࡰࡱࠦࡤࡰࡰࡨࠥࠬ੘")
bstack1l1l1l1l_opy_ = bstackl_opy_ (u"ࠪࡇࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࠢࡤࡸࠥࠨࡻࡾࠤ࠱ࠤࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡧࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡪࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡹ࠮ࠨਖ਼")
bstack1l11l1_opy_ = bstackl_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡷ࡫ࡤࡦࡰࡷ࡭ࡦࡲࡳࠡࡰࡲࡸࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡣࡧࡨࠥࡺࡨࡦ࡯ࠣ࡭ࡳࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠠࡢࡵࠣࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨࠠࡢࡰࡧࠤࠧࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠣࠢࡲࡶࠥࡹࡥࡵࠢࡷ࡬ࡪࡳࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠾ࠥࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢࠡࡣࡱࡨࠥࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠤࠪਗ਼")
bstack11l1l11_opy_ = bstackl_opy_ (u"ࠬࡓࡡ࡭ࡨࡲࡶࡲ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠢࡼࡿࠥࠫਜ਼")
bstack1ll1ll11_opy_ = bstackl_opy_ (u"࠭ࡅ࡯ࡥࡲࡹࡳࡺࡥࡳࡧࡧࠤࡪࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡹࡵࠦ࠭ࠡࡽࢀࠫੜ")
bstack1ll1ll1l_opy_ = bstackl_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠧ੝")
bstack1111l1_opy_ = bstackl_opy_ (u"ࠨࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬ࠨਫ਼")
bstack1l11l1l_opy_ = bstackl_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠠࡪࡵࠣࡲࡴࡽࠠࡳࡷࡱࡲ࡮ࡴࡧࠢࠩ੟")
bstack1l1lllll_opy_ = bstackl_opy_ (u"ࠪࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡳࡵࡣࡵࡸࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮࠽ࠤࢀࢃࠧ੠")
bstack11llll_opy_ = bstackl_opy_ (u"ࠫࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦ࡬ࡰࡥࡤࡰࠥࡨࡩ࡯ࡣࡵࡽࠥࡽࡩࡵࡪࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࢁࡽࠨ੡")
bstack1llllll_opy_ = bstackl_opy_ (u"࡛ࠬࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡦࡨࡸࡦ࡯࡬ࡴ࠼ࠣࡿࢂ࠭੢")
bstack111lll1_opy_ = bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠬ੣")
bstack1llllll1_opy_ = bstackl_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࠡࡣࡱࠤࡦࡶࡰࡳࡱࡳࡶ࡮ࡧࡴࡦࠢࡉ࡛ࠥ࠮ࡲࡰࡤࡲࡸ࠴ࡶࡡࡣࡱࡷ࠭ࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪ࠲ࠠࡴ࡭࡬ࡴࠥࡺࡨࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡱࡥࡺࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡯ࡦࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡶ࡭ࡲࡶ࡬ࡦࠢࡳࡽࡹ࡮࡯࡯ࠢࡶࡧࡷ࡯ࡰࡵࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡥࡳࡿࠠࡇ࡙࠱ࠫ੤")
bstack11111ll_opy_ = bstackl_opy_ (u"ࠨࡕࡨࡸࡹ࡯࡮ࡨࠢ࡫ࡸࡹࡶࡐࡳࡱࡻࡽ࠴࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡵ࡮ࠡࡥࡸࡶࡷ࡫࡮ࡵ࡮ࡼࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡱࡩࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࠨࡼࡿࠬ࠰ࠥࡶ࡬ࡦࡣࡶࡩࠥࡻࡰࡨࡴࡤࡨࡪࠦࡴࡰࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡂࡂ࠺࠮࠱࠰࠳ࠤࡴࡸࠠࡳࡧࡩࡩࡷࠦࡴࡰࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡼࡽ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡨࡴࡩࡳ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡲࡥ࡯࡫ࡸࡱ࠴ࡸࡵ࡯࠯ࡷࡩࡸࡺࡳ࠮ࡤࡨ࡬࡮ࡴࡤ࠮ࡲࡵࡳࡽࡿࠣࡱࡻࡷ࡬ࡴࡴࠠࡧࡱࡵࠤࡦࠦࡷࡰࡴ࡮ࡥࡷࡵࡵ࡯ࡦ࠱ࠫ੥")
bstack1l111l1l_opy_ = bstackl_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡿ࡭࡭ࠢࡩ࡭ࡱ࡫࠮࠯ࠩ੦")
bstack1l1l1l1_opy_ = bstackl_opy_ (u"ࠪࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡺࡨࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠡࠨ੧")
bstack1ll11l1l_opy_ = bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧ࠱ࠤࢀࢃࠧ੨")
bstack11l1lll_opy_ = bstackl_opy_ (u"ࠬࡋࡸࡱࡧࡦࡸࡪࡪࠠࡢࡶࠣࡰࡪࡧࡳࡵࠢ࠴ࠤ࡮ࡴࡰࡶࡶ࠯ࠤࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦ࠰ࠨ੩")
bstack1l11ll1l_opy_ = bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡇࡰࡱࠢࡸࡴࡱࡵࡡࡥ࠰ࠣࡿࢂ࠭੪")
bstack1ll1l1_opy_ = bstackl_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡲ࡯ࡢࡦࠣࡅࡵࡶ࠮ࠡࡋࡱࡺࡦࡲࡩࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡼࡿ࠱ࠫ੫")
bstack1lllll11_opy_ = bstackl_opy_ (u"ࠨࡍࡨࡽࡸࠦࡣࡢࡰࡱࡳࡹࠦࡣࡰ࠯ࡨࡼ࡮ࡹࡴࠡࡣࡶࠤࡦࡶࡰࠡࡸࡤࡰࡺ࡫ࡳ࠭ࠢࡸࡷࡪࠦࡡ࡯ࡻࠣࡳࡳ࡫ࠠࡱࡴࡲࡴࡪࡸࡴࡺࠢࡩࡶࡴࡳࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠱ࠦ࡯࡯࡮ࡼࠤࠧࡶࡡࡵࡪࠥࠤࡦࡴࡤࠡࠤࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠧࠦࡣࡢࡰࠣࡧࡴ࠳ࡥࡹ࡫ࡶࡸࠥࡺ࡯ࡨࡧࡷ࡬ࡪࡸ࠮ࠨ੬")
bstack1lllll1l_opy_ = bstackl_opy_ (u"ࠩ࡞ࡍࡳࡼࡡ࡭࡫ࡧࠤࡦࡶࡰࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࡠࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠤࡦࡸࡥࠡࡽ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡱࡣࡷ࡬ࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡤࡷࡶࡸࡴࡳ࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂࢂ࠴ࠠࡇࡱࡵࠤࡲࡵࡲࡦࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡴࡱ࡫ࡡࡴࡧࠣࡺ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡼࡽ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡨࡴࡩࡳ࠰ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲࡳ࡭ࡺࡳ࠯ࡴࡧࡷ࠱ࡺࡶ࠭ࡵࡧࡶࡸࡸ࠵ࡳࡱࡧࡦ࡭࡫ࡿ࠭ࡢࡲࡳࠫ੭")
bstack1lll1l1_opy_ = bstackl_opy_ (u"ࠪ࡟ࡎࡴࡶࡢ࡮࡬ࡨࠥࡧࡰࡱࠢࡳࡶࡴࡶࡥࡳࡶࡼࡡ࡙ࠥࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡸࡤࡰࡺ࡫ࡳࠡࡱࡩࠤࡦࡶࡰࠡࡣࡵࡩࠥࡵࡦࠡࡽ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡱࡣࡷ࡬ࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡤࡷࡶࡸࡴࡳ࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂࢂ࠴ࠠࡇࡱࡵࠤࡲࡵࡲࡦࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡴࡱ࡫ࡡࡴࡧࠣࡺ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡼࡽ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡨࡴࡩࡳ࠰ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲࡳ࡭ࡺࡳ࠯ࡴࡧࡷ࠱ࡺࡶ࠭ࡵࡧࡶࡸࡸ࠵ࡳࡱࡧࡦ࡭࡫ࡿ࠭ࡢࡲࡳࠫ੮")
bstack1ll111l_opy_ = bstackl_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡧࡰࡱࠢ࡬ࡨࠥࢁࡽࠡࡨࡲࡶࠥ࡮ࡡࡴࡪࠣ࠾ࠥࢁࡽ࠯ࠩ੯")
bstack111111l_opy_ = bstackl_opy_ (u"ࠬࡇࡰࡱࠢࡘࡴࡱࡵࡡࡥࡧࡧࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠤࡎࡊࠠ࠻ࠢࡾࢁࠬੰ")
bstack1l1l1l_opy_ = bstackl_opy_ (u"࠭ࡕࡴ࡫ࡱ࡫ࠥࡇࡰࡱࠢ࠽ࠤࢀࢃ࠮ࠨੱ")
bstack1lll11l1_opy_ = bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠠࡪࡵࠣࡲࡴࡺࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡴࡸࠠࡷࡣࡱ࡭ࡱࡲࡡࠡࡲࡼࡸ࡭ࡵ࡮ࠡࡶࡨࡷࡹࡹࠬࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡱࡣࡵࡥࡱࡲࡥ࡭ࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲࠦ࠽ࠡ࠳ࠪੲ")
from ._version import __version__
bstack11llllll_opy_ = None
CONFIG = {}
bstack11ll1l_opy_ = None
bstack1ll11111_opy_ = None
bstack1111l_opy_ = None
bstack11l1ll_opy_ = -1
bstack1lll11_opy_ = DEFAULT_LOG_LEVEL
bstack1l1ll1ll_opy_ = 1
bstack1l1111l1_opy_ = False
bstack1l11111_opy_ = bstackl_opy_ (u"ࠨࠩੳ")
bstack1ll1l1l1_opy_ = bstackl_opy_ (u"ࠩࠪੴ")
bstack1l1lll1l_opy_ = False
bstack1lll1111_opy_ = None
bstack1lll11l_opy_ = None
bstack111ll1l_opy_ = None
bstack11111l1_opy_ = None
bstack1ll1111l_opy_ = None
bstack1llll1l_opy_ = None
bstack111llll_opy_ = None
bstack1l1ll1l1_opy_ = None
bstack1llll1l1_opy_ = None
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lll11_opy_,
                    format=bstackl_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨੵ"),
                    datefmt=bstackl_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੶"))
def bstack11l1l1l_opy_():
  global CONFIG
  global bstack1lll11_opy_
  if bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ੷") in CONFIG:
    bstack1lll11_opy_ = bstack1ll11_opy_[CONFIG[bstackl_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ੸")]]
    logging.getLogger().setLevel(bstack1lll11_opy_)
def bstack1111ll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1111l1l_opy_():
  bstack1ll11ll_opy_ = bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ੹")
  bstack111l1ll_opy_ = os.path.abspath(bstack1ll11ll_opy_)
  if not os.path.exists(bstack111l1ll_opy_):
    bstack1ll11ll_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬ੺")
    bstack111l1ll_opy_ = os.path.abspath(bstack1ll11ll_opy_)
    if not os.path.exists(bstack111l1ll_opy_):
      bstack1l1ll1_opy_(
        bstack1l1l1l1l_opy_.format(os.getcwd()))
  with open(bstack111l1ll_opy_, bstackl_opy_ (u"ࠩࡵࠫ੻")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l1ll1_opy_(bstack11l1l11_opy_.format(str(exc)))
def bstack1l11l11l_opy_(config):
  bstack1lll111l_opy_ = config.keys()
  bstack11ll1ll_opy_ = []
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੼") in config:
    bstack11ll1ll_opy_ = config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੽")]
  for bstack1l1l11ll_opy_, bstack1ll11l_opy_ in bstack11l1_opy_.items():
    if bstack1ll11l_opy_ in bstack1lll111l_opy_:
      config[bstack1l1l11ll_opy_] = config[bstack1ll11l_opy_]
      del config[bstack1ll11l_opy_]
  for bstack1l1l11ll_opy_, bstack1ll11l_opy_ in bstack1l1ll_opy_.items():
    for platform in bstack11ll1ll_opy_:
      if isinstance(bstack1ll11l_opy_, list):
        for bstack1llll1ll_opy_ in bstack1ll11l_opy_:
          if bstack1llll1ll_opy_ in platform:
            platform[bstack1l1l11ll_opy_] = platform[bstack1llll1ll_opy_]
            del platform[bstack1llll1ll_opy_]
            break
      elif bstack1ll11l_opy_ in platform:
        platform[bstack1l1l11ll_opy_] = platform[bstack1ll11l_opy_]
        del platform[bstack1ll11l_opy_]
  for bstack1l1l11ll_opy_, bstack1ll11l_opy_ in bstack1l11l_opy_.items():
    for bstack1llll1ll_opy_ in bstack1ll11l_opy_:
      if bstack1llll1ll_opy_ in bstack1lll111l_opy_:
        config[bstack1l1l11ll_opy_] = config[bstack1llll1ll_opy_]
        del config[bstack1llll1ll_opy_]
  for bstack1llll1ll_opy_ in list(config):
    for bstack1ll111ll_opy_ in bstack1llll_opy_:
      if bstack1llll1ll_opy_.lower() == bstack1ll111ll_opy_.lower() and bstack1llll1ll_opy_ != bstack1ll111ll_opy_:
        config[bstack1ll111ll_opy_] = config[bstack1llll1ll_opy_]
        del config[bstack1llll1ll_opy_]
  return config
def bstack1l1l111_opy_(config):
  global bstack1ll1l1l1_opy_
  if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ੾") in config and str(config[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੿")]).lower() != bstackl_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭઀"):
    if not bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬઁ") in config:
      config[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ં")] = {}
    if not bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬઃ") in config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ઄")]:
      if bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧઅ") in os.environ:
        config[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪઆ")][bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩઇ")] = os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪઈ")]
      else:
        current_time = datetime.datetime.now()
        bstack1ll11l1_opy_ = current_time.strftime(bstackl_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭ઉ"))
        hostname = socket.gethostname()
        bstack1lllllll_opy_ = bstackl_opy_ (u"ࠪࠫઊ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstackl_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭ઋ").format(bstack1ll11l1_opy_, hostname, bstack1lllllll_opy_)
        config[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩઌ")][bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨઍ")] = identifier
    bstack1ll1l1l1_opy_ = config[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઎")][bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪએ")]
  return config
def bstack1llll11l_opy_(config):
  if bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬઐ") in config and config[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ઑ")] not in bstack111ll_opy_:
    return config[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ઒")]
  elif bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨઓ") in os.environ:
    return os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩઔ")]
  else:
    return None
def bstack11l1ll1_opy_(config):
  if bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪક") in config:
    return config[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫખ")]
  elif bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬગ") in os.environ:
    return os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊ࠭ઘ")]
  else:
    return None
def bstack1111l11_opy_(config):
  if bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ઙ") in config and config[bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧચ")] not in bstack111l_opy_:
    return config[bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨછ")]
  elif bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨજ") in os.environ:
    return os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩઝ")]
  else:
    return None
def bstack1ll1l11_opy_(config):
  if not bstack1111l11_opy_(config) or not bstack1llll11l_opy_(config):
    return True
  else:
    return False
def bstack1lllll1_opy_(config):
  if bstack1111ll1_opy_() < version.parse(bstackl_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨઞ")):
    return False
  if bstack1111ll1_opy_() >= version.parse(bstackl_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩટ")):
    return True
  if bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫઠ") in config and config[bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬડ")] == False:
    return False
  else:
    return True
def bstack11l11l_opy_(config, index = 0):
  global bstack1l1lll1l_opy_
  bstack1l1ll1l_opy_ = {}
  caps = bstack1l111_opy_ + bstack11lll_opy_
  if bstack1l1lll1l_opy_:
    caps += bstack1111_opy_
  if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩઢ") in config:
    for bstack111ll11_opy_ in config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪણ")][index]:
      if bstack111ll11_opy_ in caps + [bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ત"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪથ")]:
        continue
      bstack1l1ll1l_opy_[bstack111ll11_opy_] = config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭દ")][index][bstack111ll11_opy_]
  for key in config:
    if key in caps + [bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧધ")]:
      continue
    bstack1l1ll1l_opy_[key] = config[key]
  return bstack1l1ll1l_opy_
def bstack1l11ll11_opy_(config):
  global bstack1l1lll1l_opy_
  bstack1llll1_opy_ = {}
  caps = bstack11lll_opy_
  if bstack1l1lll1l_opy_:
    caps+= bstack1111_opy_
  for key in caps:
    if key in config:
      bstack1llll1_opy_[key] = config[key]
  return bstack1llll1_opy_
def bstack1111lll_opy_(bstack1l1ll1l_opy_, bstack1llll1_opy_):
  bstack1l1l1l11_opy_ = {}
  for key in bstack1l1ll1l_opy_.keys():
    if key in bstack11l1_opy_:
      bstack1l1l1l11_opy_[bstack11l1_opy_[key]] = bstack1l1ll1l_opy_[key]
    else:
      bstack1l1l1l11_opy_[key] = bstack1l1ll1l_opy_[key]
  for key in bstack1llll1_opy_:
    if key in bstack11l1_opy_:
      bstack1l1l1l11_opy_[bstack11l1_opy_[key]] = bstack1llll1_opy_[key]
    else:
      bstack1l1l1l11_opy_[key] = bstack1llll1_opy_[key]
  return bstack1l1l1l11_opy_
def bstack111l111_opy_(config, index = 0):
  global bstack1l1lll1l_opy_
  caps = {}
  bstack1llll1_opy_ = bstack1l11ll11_opy_(config)
  bstack1llll111_opy_ = bstack11lll_opy_
  if bstack1l1lll1l_opy_:
    bstack1llll111_opy_ += bstack1111_opy_
  if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨન") in config:
    if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ઩") in config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪપ")][index]:
      caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ફ")] = config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬબ")][index][bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨભ")]
    if bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬમ") in config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨય")][index]:
      caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧર")] = str(config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ઱")][index][bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩલ")])
    bstack1l1l1ll_opy_ = {}
    for bstack1ll1l1ll_opy_ in bstack1llll111_opy_:
      if bstack1ll1l1ll_opy_ in config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬળ")][index]:
        if bstack1ll1l1ll_opy_ == bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ઴"):
          bstack1l1l1ll_opy_[bstack1ll1l1ll_opy_] = str(config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧવ")][index][bstack1ll1l1ll_opy_] * 1.0)
        else:
          bstack1l1l1ll_opy_[bstack1ll1l1ll_opy_] = config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ")][index][bstack1ll1l1ll_opy_]
        del(config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩષ")][index][bstack1ll1l1ll_opy_])
    bstack1llll1_opy_.update(bstack1l1l1ll_opy_)
  bstack1l1ll1l_opy_ = bstack11l11l_opy_(config, index)
  if bstack1lllll1_opy_(config):
    bstack1l1ll1l_opy_[bstackl_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧસ")] = True
    caps.update(bstack1llll1_opy_)
    caps[bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩહ")] = bstack1l1ll1l_opy_
  else:
    bstack1l1ll1l_opy_[bstackl_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ઺")] = False
    caps.update(bstack1111lll_opy_(bstack1l1ll1l_opy_, bstack1llll1_opy_))
    if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ઻") in caps:
      caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ઼ࠬ")] = caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪઽ")]
      del(caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫા")])
    if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨિ") in caps:
      caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪી")] = caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪુ")]
      del(caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫૂ")])
  return caps
def bstack11ll11l_opy_():
  if bstack1111ll1_opy_() <= version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫૃ")):
    return bstack11l1l_opy_
  return bstack11ll1_opy_
def bstack1l111ll_opy_(options):
  return hasattr(options, bstackl_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ૄ"))
def bstack1l111lll_opy_(caps):
  browser = bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ૅ")
  if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૆") in caps:
    browser = caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ે")]
  elif bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪૈ") in caps:
    browser = caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫૉ")]
  browser = str(browser).lower()
  if browser == bstackl_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫ૊") or browser == bstackl_opy_ (u"ࠬ࡯ࡰࡢࡦࠪો"):
    browser = bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ૌ")
  if browser == bstackl_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨ્"):
    browser = bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ૎")
  if browser not in [bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ૏"), bstackl_opy_ (u"ࠪࡩࡩ࡭ࡥࠨૐ"), bstackl_opy_ (u"ࠫ࡮࡫ࠧ૑"), bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ૒"), bstackl_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧ૓")]:
    return None
  try:
    package = bstackl_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ૔").format(browser)
    name = bstackl_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩ૕")
    browser_options = getattr(__import__(package, fromlist=[name]), name)
    options = browser_options()
    if not bstack1l111ll_opy_(options):
      return None
    for bstack1llll1ll_opy_ in caps.keys():
      options.set_capability(bstack1llll1ll_opy_, caps[bstack1llll1ll_opy_])
    return options
  except Exception as e:
    logger.debug(str(e))
    return None
def bstack1l111l11_opy_(options, bstack11lll11_opy_):
  if not bstack1l111ll_opy_(options):
    return
  for bstack1llll1ll_opy_ in bstack11lll11_opy_.keys():
    options.set_capability(bstack1llll1ll_opy_, bstack11lll11_opy_[bstack1llll1ll_opy_])
  if bstackl_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨ૖") in options._caps:
    if options._caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૗")] and options._caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ૘")].lower() != bstackl_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭૙"):
      del options._caps[bstackl_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ૚")]
def bstack1l1lll11_opy_(proxy_config):
  if bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ૛") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪ૜")] = proxy_config[bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭૝")]
    del(proxy_config[bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ૞")])
  if bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧ૟") in proxy_config and proxy_config[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨૠ")].lower() != bstackl_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭ૡ"):
    proxy_config[bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪૢ")] = bstackl_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨૣ")
  if bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧ૤") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭૥")] = bstackl_opy_ (u"ࠫࡵࡧࡣࠨ૦")
  return proxy_config
def bstack1ll1lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ૧") in config:
    return proxy
  config[bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ૨")] = bstack1l1lll11_opy_(config[bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭૩")])
  if proxy == None:
    proxy = Proxy(config[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ૪")])
  return proxy
def bstack1l11l11_opy_(self):
  global CONFIG
  global bstack1l1ll1l1_opy_
  if bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ૫") in CONFIG and bstack11ll11l_opy_().startswith(bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫ૬")):
    return CONFIG[bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ૭")]
  elif bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ૮") in CONFIG and bstack11ll11l_opy_().startswith(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࠨ૯")):
    return CONFIG[bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ૰")]
  else:
    return bstack1l1ll1l1_opy_(self)
def bstack1l1ll11l_opy_():
  if bstack1111ll1_opy_() < version.parse(bstackl_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ૱")):
    logger.warning(bstack11111ll_opy_.format(bstack1111ll1_opy_()))
    return
  global bstack1l1ll1l1_opy_
  from selenium.webdriver.remote.remote_connection import RemoteConnection
  bstack1l1ll1l1_opy_ = RemoteConnection._get_proxy_url
  RemoteConnection._get_proxy_url = bstack1l11l11_opy_
def bstack111ll1_opy_(config):
  if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭૲") in config:
    if str(config[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ૳")]).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩ૴"):
      return True
    else:
      return False
  elif bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࠪ૵") in os.environ:
    if str(os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫ૶")]).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬ૷"):
      return True
    else:
      return False
  else:
    return False
def bstack1l11111l_opy_(config):
  if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ૸") in config:
    return config[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ૹ")]
  if bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩૺ") in config:
    return config[bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪૻ")]
  return {}
def bstack111l11l_opy_(caps):
  global bstack1ll1l1l1_opy_
  if bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ૼ") in caps:
    caps[bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ૽")][bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭૾")] = True
    if bstack1ll1l1l1_opy_:
      caps[bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ૿")][bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ଀")] = bstack1ll1l1l1_opy_
  else:
    caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨଁ")] = True
    if bstack1ll1l1l1_opy_:
      caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬଂ")] = bstack1ll1l1l1_opy_
def bstack1ll1111_opy_():
  global CONFIG
  if bstack111ll1_opy_(CONFIG):
    bstack11ll111_opy_ = bstack1l11111l_opy_(CONFIG)
    bstack111l1l1_opy_(bstack1llll11l_opy_(CONFIG), bstack11ll111_opy_)
def bstack111l1l1_opy_(key, bstack11ll111_opy_):
  global bstack11llllll_opy_
  logger.info(bstack1ll1ll1l_opy_)
  try:
    bstack11llllll_opy_ = Local()
    bstack1ll1l111_opy_ = {bstackl_opy_ (u"ࠬࡱࡥࡺࠩଃ"): key}
    bstack1ll1l111_opy_.update(bstack11ll111_opy_)
    logger.debug(bstack11llll_opy_.format(str(bstack1ll1l111_opy_)))
    bstack11llllll_opy_.start(**bstack1ll1l111_opy_)
    if bstack11llllll_opy_.isRunning():
      logger.info(bstack1l11l1l_opy_)
  except Exception as e:
    bstack1l1ll1_opy_(bstack1l1lllll_opy_.format(str(e)))
def bstack1lllll_opy_():
  global bstack11llllll_opy_
  if bstack11llllll_opy_.isRunning():
    logger.info(bstack1111l1_opy_)
    bstack11llllll_opy_.stop()
  bstack11llllll_opy_ = None
def bstack1ll111l1_opy_():
  logger.info(bstack1l1lll_opy_)
  global bstack11llllll_opy_
  if bstack11llllll_opy_:
    bstack1lllll_opy_()
  logger.info(bstack1l1l1lll_opy_)
def bstack1ll111_opy_(self, *args):
  logger.error(bstack1l1l1111_opy_)
  bstack1ll111l1_opy_()
def bstack1l1ll1_opy_(err):
  logger.critical(bstack1ll1ll11_opy_.format(str(err)))
  atexit.unregister(bstack1ll111l1_opy_)
  sys.exit(1)
def bstack111l1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  atexit.unregister(bstack1ll111l1_opy_)
  sys.exit(1)
def bstack11lllll1_opy_():
  global CONFIG
  CONFIG = bstack1111l1l_opy_()
  CONFIG = bstack1l11l11l_opy_(CONFIG)
  CONFIG = bstack1l1l111_opy_(CONFIG)
  if bstack1ll1l11_opy_(CONFIG):
    bstack1l1ll1_opy_(bstack1l11l1_opy_)
  CONFIG[bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ଄")] = bstack1111l11_opy_(CONFIG)
  CONFIG[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪଅ")] = bstack1llll11l_opy_(CONFIG)
  if bstack11l1ll1_opy_(CONFIG):
    CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫଆ")] = bstack11l1ll1_opy_(CONFIG)
  bstack1l1111ll_opy_()
  bstack11l1l1_opy_()
  if bstack1l1lll1l_opy_:
    CONFIG[bstackl_opy_ (u"ࠩࡤࡴࡵ࠭ଇ")] = bstack11111_opy_(CONFIG)
    logger.info(bstack1l1l1l_opy_.format(CONFIG[bstackl_opy_ (u"ࠪࡥࡵࡶࠧଈ")]))
def bstack11l1l1_opy_():
  global CONFIG
  global bstack1l1lll1l_opy_
  if bstackl_opy_ (u"ࠫࡦࡶࡰࠨଉ") in CONFIG:
    bstack1l1lll1l_opy_ = True
def bstack11111_opy_(config):
  bstack1l11lll_opy_ = bstackl_opy_ (u"ࠬ࠭ଊ")
  bstack11llll1l_opy_ = config[bstackl_opy_ (u"࠭ࡡࡱࡲࠪଋ")]
  if isinstance(config[bstackl_opy_ (u"ࠧࡢࡲࡳࠫଌ")], str):
    if os.path.splitext(bstack11llll1l_opy_)[1] in bstack1ll1l_opy_:
      if os.path.exists(bstack11llll1l_opy_):
        bstack1l11lll_opy_ = bstack1llll11_opy_(config, bstack11llll1l_opy_)
      elif bstack1l11ll_opy_(bstack11llll1l_opy_):
        bstack1l11lll_opy_ = bstack11llll1l_opy_
      else:
        bstack1l1ll1_opy_(bstack1ll1l1_opy_.format(bstack11llll1l_opy_))
    else:
      if bstack1l11ll_opy_(bstack11llll1l_opy_):
        bstack1l11lll_opy_ = bstack11llll1l_opy_
      elif os.path.exists(bstack11llll1l_opy_):
        bstack1l11lll_opy_ = bstack1llll11_opy_(bstack11llll1l_opy_)
      else:
        bstack1l1ll1_opy_(bstack1lll1l1_opy_)
  else:
    if len(bstack11llll1l_opy_) > 2:
      bstack1l1ll1_opy_(bstack1lllll11_opy_)
    elif len(bstack11llll1l_opy_) == 2:
      if bstackl_opy_ (u"ࠨࡲࡤࡸ࡭࠭଍") in bstack11llll1l_opy_ and bstackl_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ଎") in bstack11llll1l_opy_:
        if os.path.exists(bstack11llll1l_opy_[bstackl_opy_ (u"ࠪࡴࡦࡺࡨࠨଏ")]):
          bstack1l11lll_opy_ = bstack1llll11_opy_(config, bstack11llll1l_opy_[bstackl_opy_ (u"ࠫࡵࡧࡴࡩࠩଐ")], bstack11llll1l_opy_[bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ଑")])
        else:
          bstack1l1ll1_opy_(bstack1ll1l1_opy_.format(bstack11llll1l_opy_))
      else:
        bstack1l1ll1_opy_(bstack1lllll11_opy_)
    else:
      for key in bstack11llll1l_opy_:
        if key in bstack1l1l1_opy_:
          if key == bstackl_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ଒"):
            if os.path.exists(bstack11llll1l_opy_[key]):
              bstack1l11lll_opy_ = bstack1llll11_opy_(config, bstack11llll1l_opy_[key])
            else:
              bstack1l1ll1_opy_(bstack1ll1l1_opy_.format(bstack11llll1l_opy_))
          else:
            bstack1l11lll_opy_ = bstack11llll1l_opy_[key]
        else:
          bstack1l1ll1_opy_(bstack1lllll1l_opy_)
  return bstack1l11lll_opy_
def bstack1l11ll_opy_(bstack1l11lll_opy_):
  import re
  bstack1l11lll1_opy_ = re.compile(bstackl_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢଓ"))
  bstack11ll11_opy_ = re.compile(bstackl_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧଔ"))
  if bstackl_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨକ") in bstack1l11lll_opy_ or re.fullmatch(bstack1l11lll1_opy_, bstack1l11lll_opy_) or re.fullmatch(bstack11ll11_opy_, bstack1l11lll_opy_):
    return True
  else:
    return False
def bstack1llll11_opy_(config, path, bstack11lll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstackl_opy_ (u"ࠪࡶࡧ࠭ଖ")).read()).hexdigest()
  bstack1l1ll11_opy_ = bstack1l111ll1_opy_(md5_hash)
  bstack1l11lll_opy_ = None
  if bstack1l1ll11_opy_:
    logger.info(bstack1ll111l_opy_.format(bstack1l1ll11_opy_, md5_hash))
    return bstack1l1ll11_opy_
  bstack11l11ll_opy_ = MultipartEncoder(
    fields={
        bstackl_opy_ (u"ࠫ࡫࡯࡬ࡦࠩଗ"): (os.path.basename(path), open(os.path.abspath(path), bstackl_opy_ (u"ࠬࡸࡢࠨଘ")), bstackl_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪଙ")),
        bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪଚ"): bstack11lll1l_opy_
    }
  )
  response = requests.post(bstack11l11_opy_, data=bstack11l11ll_opy_,
                         headers={bstackl_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧଛ"): bstack11l11ll_opy_.content_type}, auth=(bstack1111l11_opy_(config), bstack1llll11l_opy_(config)))
  try:
    res = json.loads(response.text)
    bstack1l11lll_opy_ = res[bstackl_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪଜ")]
    logger.info(bstack111111l_opy_.format(bstack1l11lll_opy_))
    bstack1lll1ll_opy_(md5_hash, bstack1l11lll_opy_)
  except ValueError as err:
    bstack1l1ll1_opy_(bstack1l11ll1l_opy_.format(str(err)))
  return bstack1l11lll_opy_
def bstack1l1111ll_opy_():
  global CONFIG
  global bstack1l1ll1ll_opy_
  bstack1ll11lll_opy_ = 1
  if bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪଝ") in CONFIG:
    bstack1ll11lll_opy_ = CONFIG[bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫଞ")]
  bstack1l1ll111_opy_ = 0
  if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଟ") in CONFIG:
    bstack1l1ll111_opy_ = len(CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ")])
  bstack1l1ll1ll_opy_ = int(bstack1ll11lll_opy_) * int(bstack1l1ll111_opy_)
def bstack1l111ll1_opy_(md5_hash):
  bstack1l11ll1_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩଡ")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨଢ"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪଣ"))
  if os.path.exists(bstack1l11ll1_opy_):
    bstack11l111_opy_ = json.load(open(bstack1l11ll1_opy_,bstackl_opy_ (u"ࠪࡶࡧ࠭ତ")))
    if md5_hash in bstack11l111_opy_:
      bstack1lll1lll_opy_ = bstack11l111_opy_[md5_hash]
      bstack1ll1l1l_opy_ = datetime.datetime.now()
      bstack1l1l1ll1_opy_ = datetime.datetime.strptime(bstack1lll1lll_opy_[bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧଥ")], bstackl_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩଦ"))
      if (bstack1ll1l1l_opy_ - bstack1l1l1ll1_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1lll1lll_opy_[bstackl_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫଧ")]):
        return None
      return bstack1lll1lll_opy_[bstackl_opy_ (u"ࠧࡪࡦࠪନ")]
  else:
    return None
def bstack1lll1ll_opy_(md5_hash, bstack1l11lll_opy_):
  bstack1lll11ll_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠨࢀࠪ଩")), bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩପ"))
  if not os.path.exists(bstack1lll11ll_opy_):
    os.makedirs(bstack1lll11ll_opy_)
  bstack1l11ll1_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠪࢂࠬଫ")), bstackl_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫବ"), bstackl_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ଭ"))
  bstack1111111_opy_ = {
    bstackl_opy_ (u"࠭ࡩࡥࠩମ"): bstack1l11lll_opy_,
    bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪଯ"): datetime.datetime.strftime(datetime.datetime.now(), bstackl_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬର")),
    bstackl_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ଱"): str(__version__)
  }
  if os.path.exists(bstack1l11ll1_opy_):
    bstack11l111_opy_ = json.load(open(bstack1l11ll1_opy_,bstackl_opy_ (u"ࠪࡶࡧ࠭ଲ")))
  else:
    bstack11l111_opy_ = {}
  bstack11l111_opy_[md5_hash] = bstack1111111_opy_
  with open(bstack1l11ll1_opy_, bstackl_opy_ (u"ࠦࡼ࠱ࠢଳ")) as outfile:
    json.dump(bstack11l111_opy_, outfile)
def bstack1l1l11l_opy_(self):
  return
def bstack11llll11_opy_(self):
  return
def bstack1l11l111_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1lll1l1l_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11ll1l_opy_
  global bstack11l1ll_opy_
  global bstack1111l_opy_
  global bstack1l1111l1_opy_
  global bstack1l11111_opy_
  global bstack1lll1111_opy_
  CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ଴")] = str(bstack1l11111_opy_) + str(__version__)
  command_executor = bstack11ll11l_opy_()
  logger.debug(bstack1ll1ll1_opy_.format(command_executor))
  proxy = bstack1ll1lll_opy_(CONFIG, proxy)
  bstack11llll1_opy_ = 0 if bstack11l1ll_opy_ < 0 else bstack11l1ll_opy_
  if bstack1l1111l1_opy_ is True:
    bstack11llll1_opy_ = int(threading.current_thread().getName())
  bstack11lll11_opy_ = bstack111l111_opy_(CONFIG, bstack11llll1_opy_)
  logger.debug(bstack11lll1_opy_.format(str(bstack11lll11_opy_)))
  if bstack111ll1_opy_(CONFIG):
    bstack111l11l_opy_(bstack11lll11_opy_)
  if options:
    bstack1l111l11_opy_(options, bstack11lll11_opy_)
  if desired_capabilities:
    if bstack1111ll1_opy_() >= version.parse(bstackl_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬଵ")):
      desired_capabilities = {}
    else:
      desired_capabilities.update(bstack11lll11_opy_)
  if not options:
    options = bstack1l111lll_opy_(bstack11lll11_opy_)
  if (
      not options and not desired_capabilities
  ) or (
      bstack1111ll1_opy_() < version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ଶ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11lll11_opy_)
  logger.info(bstack1l1111_opy_)
  if bstack1111ll1_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧଷ")):
    bstack1lll1111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1111ll1_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩସ")):
    bstack1lll1111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lll1111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack11ll1l_opy_ = self.session_id
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ହ") in CONFIG and bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ଺") in CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଻")][bstack11llll1_opy_]:
    bstack1111l_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ଼ࠩ")][bstack11llll1_opy_][bstackl_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଽ")]
  logger.debug(bstack11ll1l1_opy_.format(bstack11ll1l_opy_))
def bstack111111_opy_(self, test):
  global CONFIG
  global bstack11ll1l_opy_
  global bstack1ll11111_opy_
  global bstack1111l_opy_
  global bstack1lll11l_opy_
  if bstack11ll1l_opy_:
    try:
      data = {}
      bstack1ll1l11l_opy_ = None
      if test:
        bstack1ll1l11l_opy_ = str(test.data)
      if bstack1ll1l11l_opy_ and not bstack1111l_opy_:
        data[bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ା")] = bstack1ll1l11l_opy_
      if bstack1ll11111_opy_:
        if bstack1ll11111_opy_.status == bstackl_opy_ (u"ࠩࡓࡅࡘ࡙ࠧି"):
          data[bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪୀ")] = bstackl_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୁ")
        elif bstack1ll11111_opy_.status == bstackl_opy_ (u"ࠬࡌࡁࡊࡎࠪୂ"):
          data[bstackl_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ୃ")] = bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୄ")
          if bstack1ll11111_opy_.message:
            data[bstackl_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ୅")] = str(bstack1ll11111_opy_.message)
      user = CONFIG[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ୆")]
      key = CONFIG[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭େ")]
      url = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩୈ").format(user, key, bstack11ll1l_opy_)
      headers = {
        bstackl_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ୉"): bstackl_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ୊"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack111lll1_opy_.format(str(e)))
  bstack1lll11l_opy_(self, test)
def bstack111l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack111ll1l_opy_
  bstack111ll1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll11111_opy_
  bstack1ll11111_opy_ = self._test
def bstack1ll11l11_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstackl_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢୋ"), bstackl_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧୌ"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstackl_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࡦ࡬ࡶ୍ࠧ"), bstackl_opy_ (u"ࠥ࠲ࠧ୎")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstackl_opy_ (u"ࠦ࠯࠴ࡸ࡮࡮ࠥ୏"))))
  if not files:
    pabot._write(bstackl_opy_ (u"ࠬ࡝ࡁࡓࡐ࠽ࠤࡓࡵࠠࡰࡷࡷࡴࡺࡺࠠࡧ࡫࡯ࡩࡸࠦࡩ࡯ࠢࠥࠩࡸࠨࠧ୐") % outs_dir, pabot.Color.YELLOW)
    return bstackl_opy_ (u"ࠨࠢ୑")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack11l111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstackl_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦ୒") in options:
    del options[bstackl_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ୓")]
  if ROBOT_VERSION < bstackl_opy_ (u"ࠤ࠷࠲࠵ࠨ୔"):
    stats = {
      bstackl_opy_ (u"ࠥࡧࡷ࡯ࡴࡪࡥࡤࡰࠧ୕"): {bstackl_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥୖ"): 0, bstackl_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧୗ"): 0, bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ୘"): 0},
      bstackl_opy_ (u"ࠢࡢ࡮࡯ࠦ୙"): {bstackl_opy_ (u"ࠣࡶࡲࡸࡦࡲࠢ୚"): 0, bstackl_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ୛"): 0, bstackl_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଡ଼"): 0},
    }
  else:
    stats = {
      bstackl_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥଢ଼"): 0,
      bstackl_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ୞"): 0,
      bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨୟ"): 0,
      bstackl_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣୠ"): 0,
    }
  if pabot_args[bstackl_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢୡ")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstackl_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣୢ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstackl_opy_ (u"ࠥࡥࡷࡺࡩࡧࡣࡦࡸࡸࠨୣ")], pabot_args[bstackl_opy_ (u"ࠦࡦࡸࡴࡪࡨࡤࡧࡹࡹࡩ࡯ࡵࡸࡦ࡫ࡵ࡬ࡥࡧࡵࡷࠧ୤")]
      )
      outputs += [
        bstack1ll11l11_opy_(
          os.path.join(outs_dir, str(index)+ bstackl_opy_ (u"ࠧ࠵ࠢ୥")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstackl_opy_ (u"ࠨࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸࠨ୦"), bstackl_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠥࡴ࠰ࡻࡱࡱࠨ୧") % index),
        )
      ]
    if bstackl_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣ୨") not in options:
      options[bstackl_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࠤ୩")] = bstackl_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠢ୪")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11111l_opy_(self, ff_profile_dir):
  global bstack11111l1_opy_
  if not ff_profile_dir:
    return None
  return bstack11111l1_opy_(self, ff_profile_dir)
def bstack1lll111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll1l1l1_opy_
  bstack11l11l1_opy_ = []
  if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୫") in CONFIG:
    bstack11l11l1_opy_ = CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୬")]
  bstack1ll1lll1_opy_ = len(suite_group) * len(pabot_args[bstackl_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ୭")] or [(bstackl_opy_ (u"ࠢࠣ୮"), None)]) * len(bstack11l11l1_opy_)
  pabot_args[bstackl_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢ୯")] = []
  for q in range(bstack1ll1lll1_opy_):
    pabot_args[bstackl_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ୰")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstackl_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦୱ")],
      pabot_args[bstackl_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧ୲")],
      argfile,
      pabot_args.get(bstackl_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ୳")),
      pabot_args[bstackl_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ୴")],
      platform[0],
      bstack1ll1l1l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstackl_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢ୵")] or [(bstackl_opy_ (u"ࠣࠤ୶"), None)]
    for platform in enumerate(bstack11l11l1_opy_)
  ]
def bstack1l11l1ll_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1111ll_opy_=bstackl_opy_ (u"ࠩࠪ୷")):
  global bstack1llll1l_opy_
  self.platform_index = platform_index
  self.bstack1l11l1l1_opy_ = bstack1111ll_opy_
  bstack1llll1l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll11ll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111llll_opy_
  if not bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ୸") in item.options:
    item.options[bstackl_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭୹")] = []
  for v in item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ୺")]:
    if bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ୻") in v:
      item.options[bstackl_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ୼")].remove(v)
  item.options[bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ୽")].insert(0, bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ୾").format(item.platform_index))
  item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ୿")].insert(0, bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ஀").format(item.bstack1l11l1l1_opy_))
  return bstack111llll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1lll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll1111l_opy_
  command[0] = command[0].replace(bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ஁"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪஂ"), 1)
  return bstack1ll1111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l111l_opy_(bstack1lll1l_opy_):
  global bstack1l11111_opy_
  bstack1l11111_opy_ = bstack1lll1l_opy_
  logger.info(bstack111lll_opy_.format(bstack1l11111_opy_.split(bstackl_opy_ (u"ࠧ࠮ࠩஃ"))[0]))
  global bstack1lll1111_opy_
  global bstack1lll11l_opy_
  global bstack111ll1l_opy_
  global bstack11111l1_opy_
  global bstack1ll1111l_opy_
  global bstack1llll1l_opy_
  global bstack111llll_opy_
  global bstack1llll1l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack111l1l_opy_(e, bstack11l1111_opy_)
  Service.start = bstack1l1l11l_opy_
  Service.stop = bstack11llll11_opy_
  webdriver.Remote.__init__ = bstack1lll1l1l_opy_
  WebDriver.close = bstack1l11l111_opy_
  if (bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ஄") in str(bstack1lll1l_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack111l1l_opy_(e, bstack1l1l111l_opy_)
    Output.end_test = bstack111111_opy_
    TestStatus.__init__ = bstack111l11_opy_
    WebDriverCreator._get_ff_profile = bstack11111l_opy_
    QueueItem.__init__ = bstack1l11l1ll_opy_
    pabot._create_items = bstack1lll111_opy_
    pabot._run = bstack1lll1l11_opy_
    pabot._create_command_for_execution = bstack1ll11ll1_opy_
    pabot._report_results = bstack11l111l_opy_
def bstack1l1lll1_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩஅ") in CONFIG and int(CONFIG[bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪஆ")]) > 1:
    logger.warn(bstack1lll11l1_opy_)
def bstack1l111l1_opy_(bstack1ll1llll_opy_, index):
  bstack1l111l_opy_(bstack1lll1_opy_)
  exec(open(bstack1ll1llll_opy_).read())
def bstack1l1l11l1_opy_():
  print(bstack1l111l1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪஇ"), help=bstackl_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ஈ"))
  parser.add_argument(bstackl_opy_ (u"࠭࠭ࡶࠩஉ"), bstackl_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫஊ"), help=bstackl_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ஋"))
  parser.add_argument(bstackl_opy_ (u"ࠩ࠰࡯ࠬ஌"), bstackl_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩ஍"), help=bstackl_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬஎ"))
  parser.add_argument(bstackl_opy_ (u"ࠬ࠳ࡦࠨஏ"), bstackl_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫஐ"), help=bstackl_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭஑"))
  bstack1l1l11_opy_ = parser.parse_args()
  try:
    bstack11lllll_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬஒ")
    if bstack1l1l11_opy_.framework:
      bstack11lllll_opy_ = bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨஓ")
    bstack1l111111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lllll_opy_)
    bstack1l1llll_opy_ = open(bstack1l111111_opy_, bstackl_opy_ (u"ࠪࡶࠬஔ"))
    bstack1l1111l_opy_ = bstack1l1llll_opy_.read()
    bstack1l1llll_opy_.close()
    if bstack1l1l11_opy_.username:
      bstack1l1111l_opy_ = bstack1l1111l_opy_.replace(bstackl_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫக"), bstack1l1l11_opy_.username)
    if bstack1l1l11_opy_.key:
      bstack1l1111l_opy_ = bstack1l1111l_opy_.replace(bstackl_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ஖"), bstack1l1l11_opy_.key)
    if bstack1l1l11_opy_.framework:
      bstack1l1111l_opy_ = bstack1l1111l_opy_.replace(bstackl_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ஗"), bstack1l1l11_opy_.framework)
    file_name = bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ஘")
    file_path = os.path.abspath(file_name)
    bstack1ll1ll_opy_ = open(file_path, bstackl_opy_ (u"ࠨࡹࠪங"))
    bstack1ll1ll_opy_.write(bstack1l1111l_opy_)
    bstack1ll1ll_opy_.close()
    print(bstack1l1l1l1_opy_)
  except Exception as e:
    print(bstack1ll11l1l_opy_.format(str(e)))
def bstack1lll1ll1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack11lllll1_opy_()
  bstack11l1l1l_opy_()
  atexit.register(bstack1ll111l1_opy_)
  signal.signal(signal.SIGINT, bstack1ll111_opy_)
  signal.signal(signal.SIGTERM, bstack1ll111_opy_)
def run_on_browserstack():
  if len(sys.argv) <= 1:
    print(bstack11l1lll_opy_)
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬச")  or sys.argv[1] == bstackl_opy_ (u"ࠪ࠱ࡻ࠭஛"):
    print(bstackl_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫஜ").format(__version__))
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ஝"):
    bstack1l1l11l1_opy_()
    return
  args = sys.argv
  bstack1lll1ll1_opy_()
  global CONFIG
  global bstack1l1ll1ll_opy_
  global bstack1l1111l1_opy_
  global bstack11l1ll_opy_
  global bstack1ll1l1l1_opy_
  bstack1l11llll_opy_ = bstackl_opy_ (u"࠭ࠧஞ")
  if args[1] == bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧட") or args[1] == bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ஠"):
    bstack1l11llll_opy_ = bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ஡")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ஢"):
    bstack1l11llll_opy_ = bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪண")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫத"):
    bstack1l11llll_opy_ = bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ஥")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ஦"):
    bstack1l11llll_opy_ = bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ஧")
    args = args[2:]
  else:
    if not bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬந") in CONFIG or str(CONFIG[bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ன")]).lower() in [bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫப"), bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭஫")]:
      bstack1l11llll_opy_ = bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭஬")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ஭")]).lower() == bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧம"):
      bstack1l11llll_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨய")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ர")]).lower() == bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪற"):
      bstack1l11llll_opy_ = bstackl_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫல")
      args = args[1:]
    else:
      bstack1l1ll1_opy_(bstack1llllll1_opy_)
  global bstack1lll1111_opy_
  global bstack1lll11l_opy_
  global bstack111ll1l_opy_
  global bstack11111l1_opy_
  global bstack1ll1111l_opy_
  global bstack1llll1l_opy_
  global bstack111llll_opy_
  global bstack1llll1l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack111l1l_opy_(e, bstack11l1111_opy_)
  bstack1lll1111_opy_ = webdriver.Remote.__init__
  bstack1llll1l1_opy_ = WebDriver.close
  if (bstack1l11llll_opy_ in [bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬள"), bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ழ"), bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩவ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack111l1l_opy_(e, bstack1l1l111l_opy_)
    bstack1lll11l_opy_ = Output.end_test
    bstack111ll1l_opy_ = TestStatus.__init__
    bstack11111l1_opy_ = WebDriverCreator._get_ff_profile
    bstack1ll1111l_opy_ = pabot._run
    bstack1llll1l_opy_ = QueueItem.__init__
    bstack111llll_opy_ = pabot._create_command_for_execution
  if bstack1l11llll_opy_ == bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩஶ"):
    bstack1ll1111_opy_()
    bstack1l1lll1_opy_()
    if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஷ") in CONFIG:
      bstack1l1111l1_opy_ = True
      bstack1l1llll1_opy_ = []
      for index, platform in enumerate(CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧஸ")]):
        bstack1l1llll1_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1l111l1_opy_, args=(args[0], index)))
      for t in bstack1l1llll1_opy_:
        t.start()
      for t in bstack1l1llll1_opy_:
        t.join()
    else:
      bstack1l111l_opy_(bstack1lll1_opy_)
      exec(open(args[0]).read())
  elif bstack1l11llll_opy_ == bstackl_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫஹ") or bstack1l11llll_opy_ == bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ஺"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack111l1l_opy_(e, bstack1l1l111l_opy_)
    bstack1ll1111_opy_()
    bstack1l111l_opy_(bstack111l1_opy_)
    if bstackl_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ஻") in args:
      i = args.index(bstackl_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭஼"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1ll1ll_opy_))
    args.insert(0, str(bstackl_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ஽")))
    pabot.main(args)
  elif bstack1l11llll_opy_ == bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫா"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111l1l_opy_(e, bstack1l1l111l_opy_)
    for a in args:
      if bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪி") in a:
        bstack11l1ll_opy_ = int(a.split(bstackl_opy_ (u"ࠬࡀࠧீ"))[1])
      if bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪு") in a:
        bstack1ll1l1l1_opy_ = str(a.split(bstackl_opy_ (u"ࠧ࠻ࠩூ"))[1])
    bstack1l111l_opy_(bstack111l1_opy_)
    run_cli(args)
  else:
    bstack1l1ll1_opy_(bstack1llllll1_opy_)