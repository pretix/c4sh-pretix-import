#!/usr/bin/env python
import json
import sys
import uuid
import dateutil.parser
from decimal import Decimal

import settings
from django.core.management import setup_environ
setup_environ(settings)

from backend.models import Ticket
from preorder.models import PreorderTicket, Preorder, PreorderPosition

TAX_RATE = 0

with open(sys.argv[1]) as f:
    data = json.load(f)

ticket_map = {}
variation_map = {}

def create_ticket(name, price):
    t = Ticket.objects.create(
        name=name, receipt_name=name, invoice_name=name,
        description=None, sale_price=price, invoice_price=price,
        tax_rate=TAX_RATE, rabate_rate=0, receipt_autoprint=False,
        invoice_autoprint=False, active=True, deleted=False,
        preorder_sold=True
    )
    pt = PreorderTicket.objects.create(
        name=name, backend_id=t.id, price=price, tax_rate=TAX_RATE,
        is_ticket=True, active=True,
    )
    return pt

for i in data['event']['items']:
    if i['variations']:
        for v in i['variations']:
            variation_map[v['id']] = create_ticket(
                "%s - %s" % (i['name'], v['name']), Decimal(v['price'])
            )
    else:
        ticket_map[i['id']] = create_ticket(
            i['name'], Decimal(i['price'])
        )

for o in data['event']['orders']:
    if o['status'] != 'p':
        continue
    po = Preorder.objects.create(
        name=o['user'], username=o['user'], user_id=0,
        additional_info=o['code'], unique_secret=str(uuid.uuid4()),
        cached_sum="", time=dateutil.parser.parse(o['datetime']),
        paid=o['status']
    )
    for op in o['positions']:
        if op['variation']:
            ticket = variation_map[op['variation']]
        else:
            ticket = ticket_map[op['item']]
        pp = PreorderPosition.objects.create(
            preorder=po, ticket=ticket, uuid=op['id'],
            redeemed=False
        )
        pp.uuid = op['id']
        pp.save()

print("Done.")
