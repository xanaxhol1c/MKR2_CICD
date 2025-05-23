import pytest
from django.urls import reverse
from gallery.models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

@pytest.mark.django_db
def test_gallery_view(client):
    category = Category.objects.create(name="Nature")
    response = client.get(reverse('main'))

    assert response.status_code == 200
    assert b"Nature" in response.content  

@pytest.mark.django_db
def test_image_detail_view(client):
    category = Category.objects.create(name="Animals")

    image_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    image = Image.objects.create(
        title="Tiger",
        image=image_file,
        created_date=date.today(),
        age_limit=12
    )

    image.categories.add(category)

    response = client.get(reverse('image_detail', kwargs={'pk': image.id}))

    assert response.status_code == 200
    assert b"Tiger" in response.content  
@pytest.mark.django_db
def test_image_detail_not_found(client):
    response = client.get(reverse('image_detail', kwargs={'pk': 999}))
    assert response.status_code == 404
