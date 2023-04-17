from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """
    Represent a menu.

    Fields:
    - name (str): The name of the menu.

    """

    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self) -> str:
        """
        Returns the name of the menu as a string.
        """
        return self.name


class MenuItem(models.Model):
    """
    Represent an item in a menu.

    Fields:
    - menu (Menu): The menu this item belongs to.
    - text (str): The text to display for the item.
    - link (str): The URL the item points to.
    - parent (MenuItem): The parent of this item, if any.
    - order (int): The order in which to display the item in the menu.

    """

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Меню", related_name="items")
    text = models.CharField(max_length=200, verbose_name="Текст пункта")
    link = models.CharField(max_length=200, verbose_name="Ссылка")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Родительский элемент",
        related_name="children",
    )
    order = models.IntegerField(verbose_name="Порядок")

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"

    def __init__(self, *args, **kwargs):
        """
        Initialize the MenuItem object.

        If the link field contains a URL pattern name, the link is replaced
        with the URL that corresponds to that name.

        """
        super().__init__(*args, **kwargs)
        if self.link and ":" in self.link:
            try:
                url = reverse(self.link)
                self.link = url
            except Exception as e:
                print(f"Error: {e}")

    def __str__(self) -> str:
        """
        Return a string representation of the MenuItem object.

        """
        return f"Элемент {self.menu.name} :: {self.text} :: {self.link}"

    def is_active(self, current_url: str) -> bool:
        """
        Return True if the item is active given the current URL, False otherwise.

        An item is active if its link matches the current URL or if one of its ancestors is active.

        """
        is_link_active = current_url.startswith(self.link)
        is_parent_link_active = self.parent is not None and not self.order and current_url.startswith(self.parent.link)
        return is_link_active or is_parent_link_active
