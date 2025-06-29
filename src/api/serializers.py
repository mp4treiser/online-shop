from rest_framework import serializers
from shop.models import Provider, ProviderRating, Order, ProductRating

class ProviderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=20)
    zip_address = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Provider.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.country = validated_data.get('country', instance.country)
        instance.zip_address = validated_data.get('zip_address', instance.zip_address)
        instance.save()
        return instance

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()
        return instance


class ProviderRatingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='provider.name', read_only=True)
    country = serializers.CharField(source='provider.country', read_only=True)

    class Meta:
        model = ProviderRating
        fields = ['id', 'provider_id', 'name', 'country', 'stars', 'title']


class ProductRatingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name', read_only=True)  # из связанного Product
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ProductRating
        fields = ['id', 'name', 'description', 'price', 'stars', 'title']