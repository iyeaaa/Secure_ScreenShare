import TensorFlow as tf

from PIL import Image

import os

def create_tf_example(image_path, annotations):

    with tf.io.gfile.GFile(image_path, 'rb') as fid:

        encoded_image_data = fid.read()

    image = Image.open(image_path)

    width, height = image.size

    filename = os.path.basename(image_path).encode('utf8')

    image_format = b'jpeg'

    xmins, ymins, xmaxs, ymaxs, classes_text, classes = [], [], [], [], [], []

    for annotation in annotations:

        class_id, x_center, y_center, bbox_width, bbox_height = map(float, annotation.split())

        x_min = (x_center - bbox_width / 2) * width

        y_min = (y_center - bbox_height / 2) * height

        x_max = (x_center + bbox_width / 2) * width

        y_max = (y_center + bbox_height / 2) * height

        xmins.append(x_min / width)

        ymins.append(y_min / height)

        xmaxs.append(x_max / width)

        ymaxs.append(y_max / height)

        classes_text.append(str(class_id).encode('utf8'))

        classes.append(int(class_id))

    tf_example = tf.train.Example(features=tf.train.Features(feature={

        'image/height': tf.train.Feature(int64_list=tf.train.Int64List(value=[height])),

        'image/width': tf.train.Feature(int64_list=tf.train.Int64List(value=[width])),

        'image/filename': tf.train.Feature(bytes_list=tf.train.BytesList(value=[filename])),

        'image/source_id': tf.train.Feature(bytes_list=tf.train.BytesList(value=[filename])),

        'image/encoded': tf.train.Feature(bytes_list=tf.train.BytesList(value=[encoded_image_data])),

        'image/format': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_format])),

        'image/object/bbox/xmin': tf.train.Feature(float_list=tf.train.FloatList(value=xmins)),

        'image/object/bbox/ymin': tf.train.Feature(float_list=tf.train.FloatList(value=ymins)),

        'image/object/bbox/xmax': tf.train.Feature(float_list=tf.train.FloatList(value=xmaxs)),

        'image/object/bbox/ymax': tf.train.Feature(float_list=tf.train.FloatList(value=ymaxs)),

        'image/object/class/text': tf.train.Feature(bytes_list=tf.train.BytesList(value=classes_text)),

        'image/object/class/label': tf.train.Feature(int64_list=tf.train.Int64List(value=classes)),

    }))

    return tf_example

def main():

    # Set your YOLOv8 annotation and image directories

    yolo_annotation_dir = '/path/to/yolo/annotations'

    image_dir = '/path/to/images'

    tfrecord_output_path = '/path/to/output.tfrecord'

    # Iterate through YOLO annotations

    with tf.io.TFRecordWriter(tfrecord_output_path) as writer:

        for filename in os.listdir(yolo_annotation_dir):

            annotation_path = os.path.join(yolo_annotation_dir, filename)

            image_path = os.path.join(image_dir, os.path.splitext(filename)[0] + '.jpg')

            with open(annotation_path, 'r') as annotation_file:

                annotations = annotation_file.readlines()

            tf_example = create_tf_example(image_path, annotations)

            writer.write(tf_example.SerializeToString())

if __name__ == '__main__':

    main()