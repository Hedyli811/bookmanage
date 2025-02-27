<script setup>
import axios from "axios";
import { reactive, ref, onMounted } from "vue";
import { ElMessageBox } from "element-plus";

const books = reactive([]);
const getStudents = () => {
  axios.get("http://localhost:5000/books").then((res) => {
    books.splice(0, books.length); // Clear the old data
    books.push(...res.data.results); // Unpack the new data
    console.log("Data updated");
  });
};

// After the page is rendered, add data
onMounted(() => {
  getStudents();
});

// Delete data
const handleDelete = (index, scope) => {

   ElMessageBox.confirm("Are you sure you want to delete this book?")
    .then(() => {
       console.log(index, scope.id);
  console.log(`http://localhost:5000/books/${scope.id}`);
  axios.delete(`http://localhost:5000/books/${scope.id}`).then(() => {
    getStudents();
  });
    })
    .catch(() => {
      console.log("deletion cancelled")
    });

};

/* Adding Form */
const add_dialog_visible = ref(false); // Control form display
const ruleFormRef = ref(); // Reference to the form object
const book_form = reactive({
  book_number: "",
  book_name: "",
  book_type: "",
  book_price: "",
  author: "",
  book_publisher: "",
  id: "",
});

// Form submit event
const submitForm = (formEl) => {
  console.log(book_form);
  axios.post("http://localhost:5000/books/", book_form).then(() => {
    add_dialog_visible.value = false;
    formEl.resetFields();
    getStudents();
  });
};

// Reset form
const resetForm = (formEl) => {
  formEl.resetFields();
};

// Confirm before closing the dialog
const handleClose = (done) => {
  ElMessageBox.confirm("Are you sure you want to close?")
    .then(() => {
      done();
    })
    .catch(() => {});
};

/* Edit Form */
const editFormRef = ref();
const edit_dialog_visible = ref(false);
const handleEdit = (index, scope) => {
  for (let key in scope) {
    book_form[key] = scope[key];
  }
  edit_dialog_visible.value = true;
};
// Edit submit button
const submitEditForm = (formEl) => {
  axios
    .put(`http://localhost:5000/books/${book_form.id}`, book_form)
    .then((res) => {
      formEl.resetFields();
      edit_dialog_visible.value = false;
      getStudents();
    });
};
</script>

<template>
  <div style="margin: 0 auto; width: 50%">
    <h1 style="text-align: center">Book Management System</h1>
    <!-- Add Book Button -->
    <el-button type="primary" @click="add_dialog_visible = true" size="small"
      >Add Book</el-button
    >
    <!-- Data Table -->
    <el-table :data="books" style="margin: 20px auto">
      <el-table-column label="Number" prop="book_number" />
      <el-table-column label="Title" prop="book_name" />
      <el-table-column label="Type" prop="book_type" />
      <el-table-column label="Price" prop="book_price" />
      <el-table-column label="Author" prop="author" />
      <el-table-column label="Publisher" prop="book_publisher" />
      <el-table-column align="right" label="Actions" width="200px">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
            Edit
          </el-button>
          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
          >
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>

  <!-- Add Book Dialog -->
  <el-dialog
    title="Add Book"
    v-model="add_dialog_visible"
    width="30%"
    :before-close="handleClose"
  >
    <el-form
      ref="ruleFormRef"
      :model="book_form"
      status-icon
      label-width="120px"
      class="demo-ruleForm"
    >
      <el-form-item label="Number" prop="book_number">
        <el-input v-model="book_form.book_number" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Title" prop="book_name">
        <el-input v-model="book_form.book_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Type" prop="book_type">
        <el-input v-model="book_form.book_type" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Price" prop="book_price">
        <el-input v-model.number="book_form.book_price" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Author" prop="author">
        <el-input v-model="book_form.author" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Publisher" prop="book_publisher">
        <el-input v-model="book_form.book_publisher" autocomplete="off" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)"
          >Submit</el-button
        >
        <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>

  <!-- Edit Book Dialog -->
  <el-dialog
    title="Edit Book"
    v-model="edit_dialog_visible"
    width="30%"
    :before-close="handleClose"
  >
    <el-form
      ref="editFormRef"
      :model="book_form"
      status-icon
      label-width="120px"
      class="demo-ruleForm"
    >
      <el-form-item label="Number" prop="book_number">
        <el-input v-model="book_form.book_number" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Title" prop="book_name">
        <el-input v-model="book_form.book_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Type" prop="book_type">
        <el-input v-model="book_form.book_type" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Price" prop="book_price">
        <el-input v-model.number="book_form.book_price" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Author" prop="author">
        <el-input v-model="book_form.author" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Publisher" prop="book_publisher">
        <el-input v-model="book_form.book_publisher" autocomplete="off" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitEditForm(editFormRef)">
          Submit
        </el-button>
        <el-button @click="resetForm(editFormRef)">Reset</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<style scoped></style>
