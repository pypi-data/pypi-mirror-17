namespace java com.baixing.yaoguang.thrift.gen
namespace py yaoguang

enum Entity {
  CONTACT = 1,
  COMPANY = 2,
  AD = 3
}

exception ThriftException {
  1: i32 code,
  2: string message
}

service ThriftInterface {
  bool isReady(1:string arg),
  string get(1: Entity entity, 2: list<string> fields, 3: list<string> ids) throws (1:ThriftException error)
}