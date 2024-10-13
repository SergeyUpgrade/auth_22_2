from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование товара",
        help_text="Введите наименование товара",
    )
    description = models.TextField(
        verbose_name="Описание товара", help_text="Введите описание товара", **NULLABLE
    )
    image = models.ImageField(
        upload_to="catalog/image",
        verbose_name="Изображение",
        help_text="Загрузите изображение",
        **NULLABLE
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Укажите категорию", **NULLABLE
    )
    price = models.IntegerField(
        verbose_name="Цена", help_text="Укажите цену", **NULLABLE
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        help_text="Введите владельца товара",
        related_name="products",
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = (
            "name",
            "category",
            "price",
        )
        permissions = (
            ("change_publication", "Можете поменять статус публикации"),
            ("change_depiction", "Можете поменять описание продукта"),
            ("change_category", "Можете поменять категорию продукта"),
        )

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(
        max_length=150,
        verbose_name="Наименование категории",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Version(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="versions",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Версия",
    )

    version_num = models.PositiveIntegerField(
        verbose_name="Номер версии",
        help_text="Укажите номер версии продукта",
        default=0,
        null=True,
        blank=True,
    )

    version_name = models.CharField(
        max_length=100,
        verbose_name="Наименование версии",
        help_text="Введите наименование версии продукта",
        default="",
        null=True,
        blank=True,
    )

    active = models.BooleanField(
        verbose_name="Признак текущей версии",
        help_text="Введите признак текущей версии продукта",
        default=False
    )

    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версии продукта"

    def __str__(self):
        return f"{self.product} {self.version_num} {self.version_name} {self.active}"