<template>
  <div class="min-h-screen p-8 bg-purple-100">
    <div class="mb-8">
      <v-select
        v-model="filterTags"
        :items="allTags"
        label="Filter by tags"
        multiple
        class="w-full mb-4 bg-white"
      ></v-select>
      <v-btn @click="applyFilter" class="w-full bg-purple-500 text-black"
        >Filter</v-btn
      >
    </div>
    <v-list class="list-none">
      <v-list-item
        v-for="(image, index) in paginatedImages"
        :key="index"
        class="mb-4 p-4 bg-white rounded shadow-lg border-2 border-purple-500 cursor-pointer"
      >
        <v-list-item-content>
          <div class="font-bold text-xl mb-2">ID: {{ image.id }}</div>
          <div class="text-gray-700 text-base">
            Tags: {{ image.tags.join(', ') }}
          </div>

 
          <v-dialog max-width="500">
            <template v-slot:activator="{ props: activatorProps }">
              <v-btn
                @click="selectImage(image)"
                v-bind="activatorProps"
                color="surface-variant"
                text="Open Dialog"
                variant="flat"
              ></v-btn>
            </template>

            <template v-slot:default="{ isActive }">
              <v-card title="image" class="bg-purple-100">
                <template v-if="loading">
                  <v-progress-circular indeterminate color="purple"></v-progress-circular>
                </template>
                <template v-if="error">
                  <v-alert type="error" class="mb-4"> {{ error }}</v-alert>
                  <v-btn color="red darken-1" text @click="fetchImage">Retry</v-btn>
                </template>
                <template v-if="actualImage">
                
                  <div v-html="actualImage"></div>
                  <v-card-title class="headline mb-2 text-purple-700">{{ image.id }}</v-card-title>
                  <v-card-text class="body-1">
                    Tags: 
                    <v-chip
                      v-for="(tag, index) in image.tags"
                      :key="index"
                      class="mr-2"
                      color="purple"
                      text-color="white"
                    >
                      {{ tag }}
                    </v-chip>
                  </v-card-text>
                </template>
          
                <v-card-actions>
                  <v-spacer></v-spacer>

                  <v-btn
                    text="Close"
                    @click="isActive.value = false;close()"
                  ></v-btn>
                </v-card-actions>
              </v-card>
            </template>
          </v-dialog>

        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-pagination
      v-model="currentPage"
      :length="totalPages"
      :total-visible="5"
      @input="page => (currentPage = page)"
      class="mt-8"
    ></v-pagination>
  </div>
</template>

<script>
import { ref, computed, nextTick, toRaw, watch } from 'vue'
import { debounce } from 'lodash'
import axios from 'axios'

export default {
  props: {
    images: {
      type: Array,
      required: true
    },
    pageSize: {
      type: Number,
      default: 10
    }
  },
  setup(props) {
    const currentPage = ref(1)
    const filterTags = ref([])
    const dialog = ref(false)
    const selectedImage = ref(null)
    const actualImage = ref(null)
    const filteredImages= ref([...props.images]) 
    const loading = ref(false)
    const error = ref(null)

    watch(
      () => props.images,
      (newImages) => {
        if (filterTags.value.length > 0) {
          filteredImages.value = newImages.filter(image =>
            filterTags.value.some(tag => image.tags.includes(tag))
          )
        } else {
          filteredImages.value = [...newImages]
        }
      },
      { immediate: true },
    )

    const selectImage = image => {
      selectedImage.value = image.id
      fetchImage()
    }

    const fetchImage = async () => {
      console.log("było wywołane")
      loading.value = true
      error.value = null
      try {
        
        console.log("było wywołane")
        console.log(selectedImage.id)
        const response = await axios.get(
          `http://localhost:8000/image/${selectedImage.value}`
        )
        if (response.status !== 200) {
          throw new Error('Failed to fetch image')
        }
        const imageData = response.data
        console.log(imageData)
        actualImage.value = jsonToSvg(imageData)
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const close = () => {
      console.log('było zamkniete')
      dialog.value = false
      console.log('1')
      error.value = null
      console.log('2')
      loading.value = false
      console.log('3')
      actualImage.value = null
      console.log('4')
      selectedImage.value = null
      console.log('5')
      console.log('było zamkniete')
    };

    const jsonToSvg = json => {
      let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${json.width} ${json.height}">`
      json.rectangles.forEach(shape => {
        svg += `<rect x="${shape.x}" y="${shape.y}" width="${shape.width}" height="${shape.height}" fill="${shape.color}" />`
      })
      svg += '</svg>'
      return svg
    }
    
    const totalPages = computed(() =>
      Math.ceil(filteredImages.value.length / props.pageSize)
    )

    const paginatedImages = computed(() => {
      const start = (currentPage.value - 1) * props.pageSize
      const end = start + props.pageSize
      return filteredImages.value.slice(start, end)
    })

    const allTags = computed(() => {
      const tags = new Set()
      props.images.forEach(image => image.tags.forEach(tag => tags.add(tag)))
      return Array.from(tags).sort()
    })

    const applyFilter = debounce(() => {
      requestAnimationFrame(() => {
        nextTick(() => {
          if (filterTags.value.length > 0) {
            filteredImages.value = props.images.filter(image =>
              filterTags.value.some(tag => image.tags.includes(tag))
            )
          } else {
            filteredImages.value = props.images
          }
        })
      })
    }, 300)

    return {
      fetchImage,
      paginatedImages,
      currentPage,
      totalPages,
      filterTags,
      allTags,
      applyFilter,
      selectedImage,
      actualImage,
      dialog,
      selectImage,
      close,
      loading,
      error
    }

  }
}

</script>