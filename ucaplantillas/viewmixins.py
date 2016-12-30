from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin as OldSuccessMessageMixin


class SuccessMessageMixin(OldSuccessMessageMixin):
    """Añade un mensaje (usando el framework messages) cuando se envía un formulario correctamente o se borra correctamente
    un elemento en una DeleteView.

    En la vista hay que definir el parámetro success_message con el mensaje a mostrar. Éste puede formatearse con
    los atributos del modelo. También está disponible un atributo adicional llamado 'str' que contendrá la
    representación __str__ del modelo.
    """

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.get_success_message(self.get_object().__dict__))
        return super().delete(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        # Las vistas de creación y modificación tienen self.object
        if hasattr(self, 'object'):
            cleaned_data['str'] = str(self.object)

        # La vista de borrado solo tiene self.get_object
        else:
            cleaned_data['str'] = str(self.get_object())

        return self.success_message % cleaned_data
