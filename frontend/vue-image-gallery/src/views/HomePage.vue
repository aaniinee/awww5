<template>
  <div>
    <v-text-field
      v-model="filter"
      label="Filter by tag"
      @input="applyFilter"
    ></v-text-field>
    <ImageList :images="displayedImages" />
    <v-pagination
      v-model="page"
      :length="pages"
      @input="changePage"
    ></v-pagination>
  </div>
</template>

<script>
import axios from 'axios';
import ImageList from '../components/ImageList.vue';

export default {
  name: 'HomePage',
  components: {
    ImageList
  },
  data() {
    return {
      images: [],
      displayedImages: [],
      filter: '',
      page: 1,
      perPage: 5,
    };
  },
  computed: {
    pages() {
      return Math.ceil(this.filteredImages.length / this.perPage);
    },
    filteredImages() {
      if (this.filter) {
        return this.images.filter(image =>
          image.tags.includes(this.filter.toLowerCase())
        );
      } else {
        return this.images;
      }
    }
  },
  methods: {
    async fetchImages() {
      const response = await axios.get('http://127.0.0.1:8000/images');
      this.images = response.data;
      this.applyFilter();
    },
    applyFilter() {
      this.changePage();
    },
    changePage() {
      const start = (this.page - 1) * this.perPage;
      const end = start + this.perPage;
      this.displayedImages = this.filteredImages.slice(start, end);
    }
  },
  mounted() {
    this.fetchImages();
  }
};
</script>
