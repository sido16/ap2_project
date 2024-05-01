import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Image Classification Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ImageClassificationPage(),
    );
  }
}

class ImageClassificationPage extends StatefulWidget {
  @override
  _ImageClassificationPageState createState() => _ImageClassificationPageState();
}

class _ImageClassificationPageState extends State<ImageClassificationPage> {
  File? _image;
  final picker = ImagePicker();
  List<dynamic>? _output;
  String? _message;

  Future getImage(ImageSource source) async {
    final pickedFile = await picker.pickImage(source: source);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
      classifyImage(_image!);
    } else {
      print('No image selected.');
    }
  }

  Future classifyImage(File image) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('http://192.168.58.130:3000/classify-image/'), // Replace with your Django backend URL
    );
    request.files.add(
      await http.MultipartFile.fromPath(
        'image',
        image.path,
      ),
    );

    try {
      var response = await request.send();
      if (response.statusCode == 200) {
        var responseData = await response.stream.bytesToString();
        print('Response data: $responseData'); // Log response data
        setState(() {
          var parsedResponse = json.decode(responseData);
          _message = parsedResponse['message'];
          _output = [{'prediction de xception': parsedResponse['prediction de xception']}];

        });
        print('Message: $_message'); // Log message
        print('Output: $_output'); // Log output
      } else {
        print('Failed to classify image. Error ${response.statusCode}');
      }
    } catch (e) {
      print('Error: $e');
    }
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Image Classification'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            _image == null
                ? Text('No image selected.')
                : Image.file(
                    _image!,
                    width: 300,
                    height: 300,
                  ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () {
                    getImage(ImageSource.camera);
                  },
                  child: Text('Take Picture'),
                ),
                ElevatedButton(
                  onPressed: () {
                    getImage(ImageSource.gallery);
                  },
                  child: Text('Select from Gallery'),
                ),
              ],
            ),
            SizedBox(height: 20),
            _message != null
                ? Column(
                    children: <Widget>[
                      Text(
                        'Message:',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      SizedBox(height: 10),
                      Text(
                        _message!,
                        style: TextStyle(fontWeight: FontWeight.bold, color: Colors.green),
                      ),
                      SizedBox(height: 20),
                      Text(
                        'Predictions:',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      SizedBox(height: 10),
                      Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: <Widget>[
    _output != null && _output!.isNotEmpty
      ? Text(
          'Prediction: ${_output![0]['prediction de xception']}',
          style: TextStyle(fontWeight: FontWeight.bold),
        )
      : Text('No predictions available'),
  ],
),

                    ],
                  )
                : Container(),
          ],
        ),
      ),
    );
  }
}
