from core.models import MenuItem
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context: dict, menu_name: str) -> str:
    """
    Render a menu of items based on the given menu name.

    It uses the `MenuItem` model to retrieve the items and renders them using the `item.html` template.

    Args:
    - context (dict): A dictionary containing the context of the template where the tag is used.
    - menu_name (str): The name of the menu to render.

    Returns:
    - str: The rendered HTML for the menu.

    """

    current_url = context["request"].path

    menu = MenuItem.objects.select_related("parent").filter(menu__name=menu_name).order_by("order")
    menu_tree = build(current_url=current_url, items=menu)
    return template.loader.render_to_string("item.html", {"items": menu_tree})


def build(current_url: str, items: list[MenuItem]) -> list[dict]:
    """
    Build  a tree structure of menu items based on the given items list and the current URL.

    Return a list of dictionaries representing each item and its children, with a flag indicating whether
    the item is currently active.

    Args:
    - current_url (str): The URL of the current page.
    - items (list[MenuItem]): A list of `MenuItem` instances to build the menu tree from.

    Returns:
    - list[dict]: A list of dictionaries representing the menu tree.

    """
    added_items: set[int] = set()
    all_items: list[MenuItem] = items

    def builder(items: list[MenuItem]) -> list[dict]:
        """
        Builds the menu tree.

        It is recursive function that takes a list of `MenuItem` instances and returns a list of
        dictionaries representing the menu tree.

        Args:
        - items (list[MenuItem]): A list of `MenuItem` instances to build the menu tree from.

        Returns:
        - list[dict]: A list of dictionaries representing the menu tree.

        """
        nonlocal added_items, all_items, current_url

        menu_tree: list[dict] = []

        for item in items:
            if item.id in added_items:
                continue

            added_items.add(item.id)
            children = [child for child in all_items if child.parent == item]

            children_builder = builder(items=children) if children else []
            children_active = any(child.get("active") for child in children_builder)

            menu_tree.append(
                {
                    "element": item,
                    "active": item.is_active(current_url=current_url) or children_active,
                    "children": children_builder,
                }
            )
        return menu_tree

    return builder(items)
