#include <iostream>
#include <string>
#include <google/protobuf/compiler/importer.h>
#include <google/protobuf/dynamic_message.h>
#include <google/protobuf/util/json_util.h>


// import error collector
class MyErrorCollector: public google::protobuf::compiler::MultiFileErrorCollector {   
    virtual void AddError(const std::string & filename, int line, int column, const std::string & message) {        
    std::cout << filename << ", " << line << ", " << column << " " << message << std::endl;
  }
};

int main() {
    google::protobuf::compiler::DiskSourceTree sourceTree;
    sourceTree.MapPath("", "D:/src/github/toolbox/protobuf_dym_compile/proto/");
    MyErrorCollector errorCollector;
    google::protobuf::compiler::Importer importer(&sourceTree, &errorCollector);
    importer.Import("pkg/schema.proto");

    // find a message descriptor from message descriptor pool
    const google::protobuf::Descriptor * descriptor = importer.pool()->FindMessageTypeByName("pkg.SearchRequest");    
    if (!descriptor){
        std::cout << "failed to find SearchRequest" << std::endl;
        exit(-1);
    }

    // list all fields
    // type is an enum FieldDescriptor.Type defined in google/protobuf/descriptor.h
    for (auto i = 0; i < descriptor->field_count(); i++) {
      auto *field = descriptor->field(i);
        std::cout << field->type() << " " << field->name() << std::endl;
    }

    // create a message dynamically
    google::protobuf::DynamicMessageFactory factory;
    const google::protobuf::Message *proto_type =
        factory.GetPrototype(descriptor);
    google::protobuf::Message* msg = proto_type->New();
    const google::protobuf::Reflection * ref = msg->GetReflection();
    ref->SetInt32(msg, descriptor->field(1), 43);
    ref->SetInt32(msg, descriptor->field(2), 64);
    
    std::string msg_json;
    google::protobuf::util::MessageToJsonString(*msg, &msg_json);
    std::cout << msg_json << std::endl;

    return 0;
}
