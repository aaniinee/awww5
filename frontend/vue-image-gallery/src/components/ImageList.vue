<template>
  <v-list>
    <v-list-item
      v-for="image in images"
      :key="image.id"
    >
      <v-list-item-content>
        <v-list-item-title>{{ image.url }}</v-list-item-title>
        <v-list-item-subtitle>{{ image.tags.join(', ') }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: 'ImageList',
  props: {
    images: Array
  }
};
</script>
