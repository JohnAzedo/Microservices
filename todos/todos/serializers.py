from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Todo, Category


class TodoSerializer(ModelSerializer):

    class Meta:
        model = Todo
        fields = ('id', 'text', 'done', 'category')
        extra_kwargs = {
            'category': {'write_only': True},
        }

    
    def update(self, instance: Todo, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        todo = Todo.objects.create(
            text=validated_data['text'],
            done=validated_data.get('done', False),
            category=validated_data.get('category', None)
        )

        return todo


class CategorySerializer(ModelSerializer):
    count_todos = SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'
    
    def get_count_todos(self, instance):
        return Todo.objects.filter(category=instance).count()

    def create(self, validated_data):
        category = Category.objects.create(
            name=validated_data['name'],
            color=validated_data['color'],
            icon_code=validated_data.get('icon', None)
        )
        return category