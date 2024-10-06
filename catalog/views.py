from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm
from catalog.models import Product
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView


# Create your views here.


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    # fields = ("name", "description", "photo", "category", "price", "created_at", "updated_at", "manufactured_at")
    success_url = reverse_lazy('catalog:products_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    # fields = ("name", "description", "photo", "category", "price", "created_at", "updated_at", "manufactured_at")
    success_url = reverse_lazy('catalog:products_list')

    def get_success_url(self):
        return reverse('catalog:products_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, extra=1)
        if self.request.method == 'POST':
            context_data["formset"] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"


