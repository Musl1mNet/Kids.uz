import datetime

from main.models import Category


def categories(request):
    categories = Category.objects.all()
    parents = {}

    for row in categories:
        if row.parent_id not in parents:
            parents[row.parent_id] = []

        parents[row.parent_id].append(row)

    def find_children_recoursive(pid, depth=0):
        if pid not in parents or depth > 1:
            return None

        children = []
        for row in parents[pid]:
            children.append({
                "category": row,
                "children": find_children_recoursive(row.id, depth + 1)
            })
        return children

    result = find_children_recoursive(None)
    sahifalar = []
    sanalar = []
    for row in result:
        if row["category"].name.lower() == "sahifalar":
            sahifalar = result.pop(result.index(row))
    for row in result:
        if row["category"].name.lower() == "sanalar":
            sanalar = result.pop(result.index(row))
    return {
        "categories": result,
        "sahifalar": sahifalar,
        "sanalar": sanalar,
        "date": datetime.datetime.now().date()
    }
