from flask import jsonify, request

from . import api
from ..models import Destination, Experience, Package


@api.route('/destinations')
def destinations():
    tag = request.args.get('tag', '').strip()
    query = Destination.query.filter_by(is_active=True)
    if tag:
        query = query.filter(Destination.tag == tag)
    items = query.order_by(Destination.sort_order, Destination.id).all()
    return jsonify({'destinations': [item.to_dict() for item in items], 'count': len(items)})


@api.route('/destinations/<int:id>')
def destination(id):
    item = Destination.query.filter_by(id=id, is_active=True).first()
    if item is None:
        return jsonify({'error': 'destination not found'}), 404

    similar = (Destination.query
               .filter(Destination.tag == item.tag, Destination.id != item.id,
                       Destination.is_active.is_(True))
               .order_by(Destination.sort_order).limit(4).all())

    payload = item.to_dict()
    payload['highlights'] = item.highlights or []
    payload['similar'] = [other.to_dict() for other in similar]
    return jsonify(payload)


@api.route('/packages')
def packages():
    items = (Package.query.filter_by(is_active=True)
             .order_by(Package.sort_order, Package.id).all())
    return jsonify({'packages': [item.to_dict() for item in items], 'count': len(items)})


@api.route('/packages/<int:id>')
def package(id):
    item = Package.query.filter_by(id=id, is_active=True).first()
    if item is None:
        return jsonify({'error': 'package not found'}), 404
    return jsonify(item.to_dict())


@api.route('/experiences')
def experiences():
    items = (Experience.query.filter_by(is_active=True)
             .order_by(Experience.sort_order, Experience.id).all())
    return jsonify({'experiences': [
        {'id': item.id, 'title': item.title, 'duration': item.duration,
         'highlights': item.highlights, 'price': item.price, 'image_url': item.image_url}
        for item in items], 'count': len(items)})
